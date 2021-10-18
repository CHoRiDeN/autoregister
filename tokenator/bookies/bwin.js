import StealthPlugin from "puppeteer-extra-plugin-stealth";
import puppeteer from "puppeteer-extra";

export default function registerBwin(bodyData, callback) {
    return new Promise((resolve, reject) => {
        const stealth = StealthPlugin();
        stealth.enabledEvasions.delete('chrome.runtime');
        stealth.enabledEvasions.delete('iframe.contentWindow');
        puppeteer
            .use(stealth)
            .launch({
                //executablePath: '/usr/bin/chromium',
                headless: false,
                args: ['--no-sandbox', '--disable-setuid-sandbox']
            })
            .then(async (browser) => {

                const page = await browser.newPage();
                await page.setDefaultNavigationTimeout(0);
                await page.goto('https://www.bwin.es/es/mobileportal/register?rurl=https:%2F%2Fsports.bwin.es%2Fes%2Fsports');
                //STEP 1
                await page.type('input[name=emailaddress]', bodyData.email);
                await page.type('#focusPassword', bodyData.password);
                await page.click('#continue');
                await page.waitForTimeout(4 * 1000);
                await page.click('#continue');

                //SETP 2
                await page.type('input[name=iddocumentnumber]', bodyData.documentNumber);
                await page.type('input[name=firstname]', bodyData.name);
                await page.type('input[name=lastname]', bodyData.surname);
                await page.type('input[name=secondlastname]', bodyData.surname2);
                await page.type('input[name=day]', bodyData.day);
                await page.type('input[name=month]', bodyData.month);
                await page.type('input[name=year]', bodyData.year);
                await page.evaluate(()=>document.querySelector('#continue').click());

                //STEP 3
                await page.type('input[name=addressline1]', bodyData.address);
                await page.type('input[name=addresscity]', bodyData.city);
                await page.type('input[name=addresszip]', bodyData.postalCode);
                await page.type('input[name=mobilenumber]', bodyData.phone);
                await page.select('select[name=addressstate]', bodyData.province.toUpperCase());

                let policiesBox = await page.$("input[name=promotionOptions]");
                await policiesBox.click();
                policiesBox = await page.$("#removerglimits");
                await policiesBox.click();
                policiesBox = await page.$("#tacacceptance");
                await policiesBox.click();
                policiesBox = await page.$("#privacypolicyaccepted");
                await policiesBox.click();


                await page.click('#submit');
                await page.waitForTimeout(4 * 1000);
                await page.evaluate(()=>document.querySelector('#submit').click());
                await page.waitForTimeout(20 * 1000);
                let errors = (await page.$('.theme-error-i')) || undefined;
                if (errors) {
                    await page.waitForSelector('.header-ctrl-txt');
                    let headerElem = await page.$('.header-ctrl-txt');
                    let headerValue = await page.evaluate(el => el.textContent, headerElem);
                    console.log(headerValue);
                    if(headerValue == 'Verifica tu identidad'){
                        resolve('Pending verification');
                        await browser.close();
                        return;
                    }
                    await page.waitForSelector('.cms-container');
                    let element = await page.$('.cms-container');
                    let value = await page.evaluate(el => el.textContent, element);
                    reject(value);
                    await browser.close();
                }else{
                    console.log(page.url());
                    resolve('Registered');
                    await browser.close();
                    return;
                }



            });
    });
}
