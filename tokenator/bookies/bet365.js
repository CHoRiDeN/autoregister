import StealthPlugin from "puppeteer-extra-plugin-stealth";
import puppeteer from "puppeteer-extra";

export default function register(bodyData, callback) {
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
                await page.goto('https://members.bet365.es/members/services/openaccount/?hostedBy=MEMBERS_HOST&prdid=1');


                await page.type('#DniNieNumber', bodyData.documentNumber);
                await page.type('#FirstName', bodyData.name);
                await page.type('#Surname', bodyData.surname);
                await page.type('#Surname2', bodyData.surname2);
                await page.select('#DateOfBirthDay', bodyData.day);
                await page.select('#DateOfBirthMonth', bodyData.month);
                await page.select('#DateOfBirthYear', bodyData.year);
                await page.type('#EmailAddress', bodyData.email);
                await page.type('#PhoneNumber', bodyData.phone);


                await page.type('#CurrentBuildingNumberSearch', bodyData.address);
                await page.type('#CurrentStreetNameSearch', bodyData.address);
                await page.type('#CurrentPostcodeSearch', bodyData.postalCode);

                await page.click('#CurrentFindAddress');

                await page.waitForTimeout(4 * 1000);


                let producttype = (await page.$('.addressButtons')) || undefined;

                if (!producttype) {
                    console.log('no modal');
                } else {
                    console.log('handling modal addressess');
                    const elHandleArray = await page.$$('.addressButtons');
                    await elHandleArray[0].click();
                }

                await page.select('#FiscalResidence', bodyData.fiscalResidenceId);
                await page.type('#UserName', bodyData.usename);
                await page.type('#Password', bodyData.password);
                await page.type('#FourDigitPin', "1123");
                await page.type('#FourDigitPinConfirmed', "1123");
                await page.type('#FourDigitPinConfirmed', "1123");
                const radioCheckbox = await page.$("#NoThanksRadio");
                await radioCheckbox.click();
                const policiesBox = await page.$("#PoliciesAcceptance");
                await policiesBox.click();

                //check que no haya errores
                const elHandleArray = await page.$$('.su-flexiField_Error');
                const numErrors = elHandleArray.length;
                if (numErrors > 0) {
                    let errorsString = '';
                    for (let i = 0; i < numErrors; i++) {
                        console.log(elHandleArray[i]);
                        let errorText = await page.evaluate(el => el.textContent, elHandleArray[i]);
                        errorsString = errorsString + errorText;
                    }
                    reject('Hay ' + numErrors + ' errores: ' + errorsString);
                }

                page.click('#Submit');
                await page.waitForTimeout(4 * 1000);
                page.waitForNavigation({waitUntil: 'networkidle2'})

                let errors = (await page.$('.submitErrorsLightBoxContainer')) || undefined;
                if (errors) {
                    let errorElement = await page.$('.lightBoxHeader h1');
                    let value = await page.evaluate(el => el.textContent, errorElement);
                    reject(value);
                    await browser.close();
                } else {
                    resolve('Registered');
                    await browser.close();

                }

            });
    });
}



