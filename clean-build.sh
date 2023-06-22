#! /bin/bash
cd syntest-core
rm -rf node_modules
npm i
npm run build

cd ../syntest-javascript
rm -rf node_modules
npm i
./link.sh
npm run build

cd ../syntest-javascript-benchmark
rm -rf node_modules
npm i

npx syntest javascript test
