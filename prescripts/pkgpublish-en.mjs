import { writeFile } from 'fs';
const pkgfile = {
    "name": "sinzmise-cetastories-en",
    "version": "2.0.0-"+new Date().getTime()
}
writeFile('./public-en/package.json', JSON.stringify(pkgfile), function (err) {
    if (err) {
        console.log(err);
    }
    console.log("Package.json file is created successfully.");
})