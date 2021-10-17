import {createServer} from 'http';

import puppeteer from 'puppeteer-extra';
import StealthPlugin from 'puppeteer-extra-plugin-stealth';



const server = createServer((req, res) => {
    if (req.url === '/bet365') {

        const stealth = StealthPlugin();
        stealth.enabledEvasions.delete('chrome.runtime');
        stealth.enabledEvasions.delete('iframe.contentWindow');
        puppeteer
            .use(stealth)
            .launch({
                executablePath: '/usr/bin/chromium-browser',
                headless: false,
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            })
            .then(async (browser) => {

                const page = await browser.newPage();
                await page.setDefaultNavigationTimeout(0);
                await page.goto('https://members.bet365.es/members/services/openaccount/?hostedBy=MEMBERS_HOST&prdid=1');
                await page.waitForNavigation({
                    waitUntil: 'networkidle0',
                });


                await page.type('.flexiField_Input', '46478514E')
                await page.screenshot({ path: screenshot })
                console.log('See screenshot: ' + screenshot)






                await browser.close();
            });


    }
});

var port = 5006
server.listen(port);
console.log(`Node.js web server at port ${port} is running..`);


