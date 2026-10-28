/* Signature « ad-hoc » de l'app Mac (sans compte Apple payant).
   Sans signature, macOS sur puces Apple (M1/M2/M3…) affiche « est endommagé et ne peut pas être ouvert ». */
const { execFileSync } = require("child_process");
const path = require("path");
exports.default = async function (ctx) {
  if (ctx.electronPlatformName !== "darwin") return;
  const app = path.join(ctx.appOutDir, ctx.packager.appInfo.productFilename + ".app");
  console.log("  • signature ad-hoc :", app);
  try { execFileSync("xattr", ["-cr", app]); } catch (e) {}
  execFileSync("codesign", ["--force", "--deep", "--sign", "-", app], { stdio: "inherit" });
  execFileSync("codesign", ["--verify", "--deep", "--strict", app], { stdio: "inherit" });
};
