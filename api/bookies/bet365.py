from flask_restful import Resource, request
import requests
import json
from bs4 import BeautifulSoup
import urllib.parse



def getPIRXTcTokens():
    url = "http://tokenator:5006/bet365"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)
    json_response = json.loads(response.text)
    return json_response

def getPSTKToken():
    print("#### GETTING PSTK ####")
    url = "https://www.bet365.es/defaultapi/sports-configuration?_h=wOWZC7b5g2O4lxxyuCOkoQ=="

    payload = {}
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'Origin': 'https://www.bet365.es',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.bet365.es/',
        'Accept-Language': 'es,en-US;q=0.9,en;q=0.8,ca;q=0.7',
        'Cookie': 'aps03=ct=171&lng=3'
    }


    response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)

    if not 'pstk' in response.cookies:
        return False

    pstk = response.cookies['pstk']
    return pstk


def getVerifTokens():
    url = "https://members.bet365.es/members/services/openaccount/?hostedBy=MEMBERS_HOST&prdid=1"

    payload = {}
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Accept-Language': 'es'
    }

    response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)

    cookies = response.cookies.get_dict()
    keys = list(cookies.keys())

    soup = BeautifulSoup(response.text, features="html.parser")
    input_elem = soup.find("input", {"name": "__RequestVerificationToken"})
    second_token = input_elem.get('value')
    return [second_token, keys[1] + "=" + cookies[keys[1]]]


def checkNickname(nickname, token1, token2, pstk):

    print("##### CHECKING NICKNAME "+nickname+" #######")
    url = "https://members.bet365.es/members/services/OpenAccount/ValidateUsername?prdid=1&hostedBy=MEMBERS_HOST"

    payload = "firstName=asdasd&surname=adasd&username="+nickname+"&countryId=171"
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        '__RequestVerificationToken': token1,
        'sec-ch-ua-platform': '"macOS"',
        'Origin': 'https://members.bet365.es',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://members.bet365.es/members/services/openaccount/?hostedBy=MEMBERS_HOST&prdid=1',
        'Accept-Language': 'es',
        'Cookie': 'rmbs=3; ' + token2 + '; pstk=' + pstk
    }

    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
    json_response = json.loads(response.text)

    # check has those values
    is_valid = json_response['isValid']
    is_duplicated = json_response['isDuplicate']
    valid_nickname = False
    if is_valid and not is_duplicated:
        valid_nickname = True
        print("##### NICKNAME OK #######")

    return valid_nickname


def checkAddressLine(address, token1, token2, pstk):
    print("##### CHECKING ADDRESS LINE #######")

    url = "https://members.bet365.es/members/services/OpenAccount/ValidatePoBox?prdid=1&hostedBy=MEMBERS_HOST"
    payload = "CountryId=171&Value="
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        '__RequestVerificationToken': token1,
        'sec-ch-ua-platform': '"macOS"',
        'Origin': 'https://members.bet365.es',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://members.bet365.es/members/services/openaccount/?hostedBy=MEMBERS_HOST&prdid=1',
        'Accept-Language': 'es',
        'Cookie': 'rmbs=3; '+token2+'; pstk='+pstk
    }

    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
    json_response = json.loads(response.text)
    print("##### VALID: "+str(json_response['isValid']))
    return json_response['isValid']


def doRegisterCall(userdata, token1, token2, pstk):

    username = userdata['userName']
    dniNieNumber = userdata['dniNieNumber']

    url = "https://members.bet365.es/members/services/OpenAccount/Create?rurl=&prdid=1&hostedBy=MEMBERS_HOST"

    payload = "country=171&title=4&firstName=JOSE%20MARIA&surname=SANTEUGINI&surname2=SOLIS&nationalityId=170&dniNieNumber="+dniNieNumber+"&dateOfBirth=1967-08-19T00%3A00%3A00.000Z&emailAddress=read%40asddsa.com&dialingCode=%2B34&phoneNumber=667456456&requiresPreviousOrPermanentAddress=false&currentAddress%5BaddressLine1%5D=jardina+70&currentAddress%5BaddressLine2%5D=direccion2&currentAddress%5BaddressLine3%5D=rtes&currentAddress%5BtownCity%5D=Martorell&currentAddress%5BstateRegion%5D=Barcelona&currentAddress%5Bpostcode%5D=38293&currentAddress%5BenteredManually%5D=true&currentAddress%5BcountryId%5D=171&fiscalResidence=4&aaMatchTypeId=0&userName="+username+"&password=Jus65u0021ss&passwordConfirmed=Jus65u0021ss&fourDigitPin=1123&fourDigitPinConfirmed=1123&expectedMonthlySpend=-1&placeOfIssue=&bonusCode=&issuingAuthority=&dateOfIssue=&expiryDate=&originatingUrl=https%3A%2F%2Fwww.bet365.es%2F&productId=1&screenSize=1920+x+1080&currentRequestContext=NewUser&isMigratedUser=false&AcceptedMarketing=&AcceptedClientContract=&AcceptedPrivacyPolicyAndCookiePolicy=&AcceptedTermsRulesAgeKyc=&AcceptedStandardPolicies=true&AcceptedDeclaration=&AcceptedRestrictedAccess=&AcceptedResidentCheck=&AcceptedRussiaTaxCheck=&GdprNotification=false&GdprTextMessage=false&GdprEmail=false&GdprWebMessage=false&UserAcceptedDepositLimitOptOut=false"
    headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        '__RequestVerificationToken': token1,
        'sec-ch-ua-platform': '"macOS"',
        'Origin': 'https://members.bet365.es',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://members.bet365.es/members/services/openaccount/?hostedBy=MEMBERS_HOST&prdid=1',
        'Accept-Language': 'es',
        'Cookie': 'rmbs=3; ' + token2 + '; pstk=' + pstk
    }

    response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)
    print(response)
    print(response.text)
    if response.status_code != 200:
        return False
    json_response = json.loads(response.text)
    return json_response


class CheckNickname(Resource):
    def get(self):
        username = request.get_json()['userName']

        [token1, token2] = getVerifTokens()
        pstk = getPSTKToken()

        valid_nickname = checkNickname(username, token1, token2,pstk)

        return {
                   'token1': token1,
                   'token2': token2,
                    'pstk': pstk,
                   'nickname': username,
                   'isValid': valid_nickname
               }, 200

class Register(Resource):
    def get(self):
        request_data = request.get_json()

        [token1, token2] = getVerifTokens()
        pstk = getPSTKToken()
        nicknameValid = checkNickname(request_data['userName'], token1, token2,pstk)
        if not nicknameValid:
            return {
                "result": "Nickname invalid"
            }
        registerResult = doRegisterCall(request_data,token1,token2,pstk)



        return {
                "validUsernam": nicknameValid,
                   "result": registerResult
               }, 200
