#!/usr/bin/env python3
"""Adapte le projet Android généré par `npx cap add android` :
 - orientation paysage,
 - plein écran immersif (barres système masquées),
 - numéro de version pris depuis la variable VERSION (ex. 1.2.0).
Exécuté automatiquement par GitHub Actions (et par `npm run android:add`)."""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AND = os.path.join(ROOT, "android")
cfg = json.load(open(os.path.join(ROOT, "capacitor.config.json"), encoding="utf8"))
APP_ID = cfg["appId"]
ok = True

def warn(msg):
    global ok
    ok = False
    print("ATTENTION :", msg, file=sys.stderr)

# 1) Manifeste : orientation paysage
mf = os.path.join(AND, "app/src/main/AndroidManifest.xml")
try:
    s = open(mf, encoding="utf8").read()
    if "screenOrientation" not in s:
        s2, n = re.subn(r"(<activity\b)", r'\1\n            android:screenOrientation="sensorLandscape"', s, count=1)
        if n != 1:
            raise RuntimeError("balise <activity> introuvable")
        s = s2
    open(mf, "w", encoding="utf8").write(s)
    print("Manifeste : orientation paysage OK")
except Exception as e:
    warn("manifeste non modifié (%s)" % e)

# 2) MainActivity : plein écran immersif
pkg_dir = os.path.join(AND, "app/src/main/java", *APP_ID.split("."))
found = glob.glob(os.path.join(AND, "app/src/main/java/**/MainActivity.java"), recursive=True)
target = found[0] if found else os.path.join(pkg_dir, "MainActivity.java")
os.makedirs(os.path.dirname(target), exist_ok=True)
pkg = os.path.relpath(os.path.dirname(target), os.path.join(AND, "app/src/main/java")).replace(os.sep, ".")
open(target, "w", encoding="utf8").write("""package %s;

import android.os.Bundle;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        hideSystemBars();
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) hideSystemBars();
    }

    private void hideSystemBars() {
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        WindowInsetsControllerCompat c = new WindowInsetsControllerCompat(getWindow(), getWindow().getDecorView());
        c.hide(WindowInsetsCompat.Type.systemBars());
        c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    }
}
""" % pkg)
print("MainActivity :", target)

# 3) Version
ver = os.environ.get("VERSION", "").strip().lstrip("v")
gr = os.path.join(AND, "app/build.gradle")
if ver and re.fullmatch(r"\d+\.\d+\.\d+", ver):
    try:
        a, b, c = (int(x) for x in ver.split("."))
        code = a * 10000 + b * 100 + c
        s = open(gr, encoding="utf8").read()
        s, n1 = re.subn(r"versionCode\s+\d+", "versionCode %d" % code, s, count=1)
        s, n2 = re.subn(r'versionName\s+"[^"]*"', 'versionName "%s"' % ver, s, count=1)
        if n1 != 1 or n2 != 1:
            raise RuntimeError("versionCode/versionName introuvables")
        open(gr, "w", encoding="utf8").write(s)
        print("Version Android :", ver, "(code %d)" % code)
    except Exception as e:
        warn("version non modifiée (%s)" % e)

sys.exit(0 if ok else 0)  # ne bloque jamais la fabrication : l'APK reste valable sans ces réglages
