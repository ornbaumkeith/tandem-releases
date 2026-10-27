"""Stage only explicitly approved public assets, never private source/signing files."""
import hashlib,json,pathlib,urllib.request,urllib.parse,zipfile,stat
root=pathlib.Path(__file__).resolve().parent.parent
manifest=json.loads((root/'distribution/manifest.json').read_text())
assert manifest['version']=='0.5.14'
assert set(manifest['platforms'])=={'windows','android'}
out=root/'public-assets';out.mkdir()
seen=set()
for platform,item in manifest['platforms'].items():
    url=urllib.parse.urlsplit(item['url'])
    assert url.scheme=='https' and url.hostname.endswith('.oaiusercontent.com')
    archive=root/(platform+'.zip')
    with urllib.request.urlopen(item['url'],timeout=120) as response,archive.open('wb') as dest:
        total=0
        while chunk:=response.read(1024*1024):
            total+=len(chunk);assert total<400_000_000
            dest.write(chunk)
    assert hashlib.sha256(archive.read_bytes()).hexdigest()==item['archive_sha256']
    with zipfile.ZipFile(archive) as z:
        names=z.namelist();assert len(names)==len(set(names))
        assert all('/' not in n and '\\' not in n and n not in ('.','..') for n in names)
        assert all(not stat.S_ISLNK(x.external_attr>>16) for x in z.infolist())
        for name,expected in item['files'].items():
            assert name in names and name not in seen;seen.add(name)
            allowed={'Tandem_0.5.14_Windows_x64_Setup.exe','Tandem_0.5.14_Windows_x64_Setup.exe.sha256','windows-smoke.json'} if platform=='windows' else {'Tandem_0.5.14_Android.apk','Tandem_0.5.14_Android.apk.sha256','android-signature.txt','android-package.txt','android-permissions.txt','android-launch.txt','android-runtime-errors.txt','android-ui.xml'}
            assert name in allowed
            data=z.read(name)
            assert hashlib.sha256(data).hexdigest()==expected,(name,'checksum mismatch')
            (out/name).write_bytes(data)
for name in ['Tandem_0.5.14_Windows_x64_Setup.exe','Tandem_0.5.14_Android.apk']:
    p=out/name;assert p.is_file()
    expected=(out/(name+'.sha256')).read_text(encoding='utf-8-sig').split()[0]
    assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
assert (out/'Tandem_0.5.14_Windows_x64_Setup.exe').read_bytes()[:2]==b'MZ'
with zipfile.ZipFile(out/'Tandem_0.5.14_Android.apk') as apk:
    assert 'AndroidManifest.xml' in apk.namelist()
smoke=json.loads((out/'windows-smoke.json').read_text())
assert smoke['ok'] and not smoke['hasNode'] and smoke['version']=='0.5.14' and smoke['platform']=='win32'
assert "name='com.tandem.goals' versionCode='514' versionName='0.5.14'" in (out/'android-package.txt').read_text()
assert 'application-debuggable' not in (out/'android-package.txt').read_text()
assert 'Verified' in (out/'android-signature.txt').read_text()
assert 'Sign in' in (out/'android-ui.xml').read_text()
assert 'com.tandem.goals' in (out/'android-launch.txt').read_text()
errors=(out/'android-runtime-errors.txt').read_text()
assert not any(s in errors for s in ['FATAL EXCEPTION','TypeError:','ReferenceError:','Error:'])
for s in ['CAMERA','RECORD_AUDIO','READ_EXTERNAL_STORAGE','WRITE_EXTERNAL_STORAGE','READ_MEDIA_IMAGES','READ_MEDIA_VIDEO','SYSTEM_ALERT_WINDOW']:
    assert 'android.permission.'+s not in (out/'android-permissions.txt').read_text()
(out/'TESTING.md').write_bytes((root/'TESTING.md').read_bytes())
(out/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(out.iterdir())))
print('Verified both native packages, checksums, and build/launch evidence; staged only public release files.')
