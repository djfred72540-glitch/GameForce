/* Signature « ad-hoc » de l'app Mac (sans compte Apple payant). */
const { execFileSync } = require("child_process");
const path = require("path");
exports.default = async function (ctx) {
  if (ctx.electronPlatformName !== "darwin") return;
  const app = path.join(ctx.appOutDir, ctx.packager.appInfo.productFilename + ".app");
  console.log("  • signature ad-hoc :", app);
  try { execFileSync("xattr", ["-cr", app]); } catch (e) {}
  execFileSync("codesign", ["--force", "--deep", "--sign", "-", app], { stdio: "inherit" });
  try { execFileSync("codesign", ["--verify", "--deep", app], { stdio: "inherit" }); }
  catch (e) { console.warn("  • vérification codesign ignorée :", e.message); }
};
