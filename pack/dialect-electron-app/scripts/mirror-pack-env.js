/**
 * 打包前将 pack-env 镜像到 pack-env-staging，避免 electron-builder 复制时
 * 因杀毒/索引占用源目录中的 DLL 导致 EBUSY。
 */
const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const root = path.join(__dirname, '..');
const src = path.join(root, 'pack-env');
const dest = path.join(root, 'pack-env-staging');

if (!fs.existsSync(src)) {
  console.error('缺少 pack-env 目录，无法镜像。');
  process.exit(1);
}

console.log('正在镜像 pack-env -> pack-env-staging（robocopy，可重试）...');
// robocopy 成功时退出码常为 1-7（非 0），不能用 execSync 默认抛错
const cmd = `robocopy "${src}" "${dest}" /MIR /R:10 /W:3 /MT:4 /NFL /NDL /NJH /NJS /XD __pycache__`;
const result = spawnSync(cmd, {
  stdio: 'inherit',
  shell: true,
  cwd: root,
  encoding: 'utf-8'
});
const code = result.status;
if (code === null || code >= 8) {
  console.error('robocopy 失败，退出码:', code);
  process.exit(1);
}
console.log('镜像完成（robocopy 码 ' + code + '）。');
