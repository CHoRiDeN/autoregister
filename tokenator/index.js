import {createServer} from 'http';
import registerB365 from './bookies/bet365.js'
import registerBwin from './bookies/bwin.js'
import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';


const server = createServer((req, res) => {
    if (req.url === '/bet365') {
        var body = "";
        req.on("data", function (chunk) {
            body += chunk;
            let bodyData = JSON.parse(body);
            console.log(bodyData.documentNumber);

            registerB365(bodyData).then(response =>{
                res.writeHead(200);
                res.end(response);
            }).catch(ex =>{
                res.writeHead(500);
                res.end('Error:'+ ex.toString());
            })

        });
    }

    if (req.url === '/bwin') {
        var body = "";
        req.on("data", function (chunk) {
            body += chunk;
            let bodyData = JSON.parse(body);
            console.log(bodyData.documentNumber);

            registerBwin(bodyData).then(res =>{
                res.writeHead(200);
                res.end('Done');
            }).catch(ex =>{
                res.writeHead(500);
                res.end('Error:'+ ex.toString());
            })

        });
    }
});

var port = 5006
server.listen(port);
console.log(`Node.js web server at port ${port} is running..`);


