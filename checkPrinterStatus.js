
var e = require('child_process');
var dellOldPrinterPages = null;
var dellCommand = "snmpget -v2c -O vq -c public 192.168.1.10 SNMPv2-SMI::mib-2.43.10.2.1.4.1.1";

var kyoceraOldPrinterPages = null;
var kyoceraCommand = "snmpget -v2c -O vq -c public 192.168.1.11 SNMPv2-SMI::enterprises.1347.43.10.1.1.12.1.1";


var tempLastKyoPrinterLages = null;
function calculateRoundedPrice(price) {
    if (typeof (price) == "number") {
        price = (Math.ceil(price * 20) / 20).toFixed(2);
        var priceString = price.toString();
        var priceParts = priceString.split(".");
        if (priceParts.length > 1) {
            if (priceParts[1].length == 1) {
                priceString += "0";
            }
        }
        if (priceParts.length == 1) {
            priceString += ",00";
        }
        priceString.replace(".", ",");
        priceString += "€";
        return priceString;
    } else {
        return "0,00€";
    }
}

function setDellPrice(price="ERROR"){
    var priceString = calculateRoundedPrice(price);
    var priceElement = document.getElementById("dellPrice");
    if (priceElement != undefined) {
        priceElement.innerHTML = priceString;
    }
}
function setKyoPrice(price="ERROR"){
    var priceString = calculateRoundedPrice(price);
    var priceElement = document.getElementById("kyoPrice");
    if (priceElement != undefined) {
        priceElement.innerHTML = priceString;
    }
}

function setPrice(price = "ERROR") {
    var priceString = calculateRoundedPrice(price);
    var priceElement = document.getElementById("price");
    if (priceElement != undefined) {
        priceElement.innerHTML = priceString;
    }
}

function setDellPages(pages) {
    if (pages != undefined && pages != null) {
        var pagesElement = document.getElementById("dellPages");
        if (pagesElement != undefined) {
            pagesElement.innerHTML = pages;
        }
    }
}

function setKyoPages(pages) {
    if (pages != undefined && pages != null && isNaN(pages) == false) {
        var pagesElement = document.getElementById("kyoPages");
        if (pagesElement != undefined) {
            pagesElement.innerHTML = pages;
        }
    }
}

async function setup() {
    reset();
    setInterval(() => {
        // toggleNotice();
        updateData();
    }, 3500);
}
setup();

function reset() {
    try{
    e.exec(dellCommand, function (err, stdout, stderr) {
        var pagesNumber = null;
        if (stdout != undefined && stdout != null) {
            stdout = stdout.replace("\n", "");
            pagesNumber = parseInt(stdout);
        }
        if (stderr != undefined && stderr != null && typeof (stderr) == "number") {
            pagesNumber = parseInt(stderr);
        }
        if (pagesNumber != undefined && pagesNumber != null) {
            dellOldPrinterPages = pagesNumber;
        } else {
            console.log("error resetting DELL");
        }

    });
    } catch(e){
        console.log(e);
    }
    try{
    e.exec(kyoceraCommand, function (err, stdout, stderr) {
        var pagesNumber = null;
        if (stdout != undefined && stdout != null) {
            stdout = stdout.replace("\n", "");
            pagesNumber = parseInt(stdout);
        }
        if (stderr != undefined && stderr != null && typeof (stderr) == "number") {
            pagesNumber = parseInt(stderr);
        }
        if (pagesNumber != undefined && pagesNumber != null) {
            kyoceraOldPrinterPages = pagesNumber;
        } else {
            console.log("error resetting KYOCERA");
        }

    });
    } catch (e){
        console.log(e);
        if(tempLastKyoPrinterLages!=undefined&&tempLastKyoPrinterLages!=null){
            kyoceraOldPrinterPages = tempLastKyoPrinterLages;
        }
    }

    setPrice(0);
    setDellPages(0);
    setDellPrice(0);
    setKyoPages(0);
    setKyoPrice(0);

}

async function updateData() {
    try {
        var dellPages = await getDellData();
        var dellprice = null;
        if (dellPages != undefined && dellPages != null && dellPages != false) {
            setDellPages(dellPages);
            dellprice = dellPages * 0.02;
            setDellPrice(dellprice);

        }
        var kyoPages = await getKyoData();
        var kyoprice = null;
        if (kyoPages != undefined && kyoPages != null && kyoPages != false) {
            setKyoPages(kyoPages);
            kyoprice = kyoPages * 0.02;
            setKyoPrice((kyoprice/100));
        }
        var price = (dellPages + kyoPages) *0.02;
        setPrice(price);
    } catch (e) {
        console.log("error getting pages");
    }

}

async function getDellData() {
    return new Promise((resolve, reject) => {
        e.exec(dellCommand, function (err, stdout, stderr) {
            var pagesNumber = null;

            if (stdout != undefined && stdout != null) {
                stdout = stdout.replace("\n", "");
                pagesNumber = parseInt(stdout);
            }
            if (stderr != undefined && stderr != null && typeof (stderr) == "number") {
                pagesNumber = parseInt(stderr);
            }

            if (pagesNumber != undefined && pagesNumber != null && pagesNumber != "") {
                if (dellOldPrinterPages == null) {
                    dellOldPrinterPages = pagesNumber;
                }
                var pages = pagesNumber - dellOldPrinterPages;
                resolve(pages);
                return;
            } else {
                resolve(false);
                return;
            }
            // })

        });

    });
}


async function getKyoData() {
    return new Promise((resolve, reject) => {
        e.exec(kyoceraCommand, function (err, stdout, stderr) {
            var pagesNumber = null;
            if (stdout != undefined && stdout != null) {
                stdout = stdout.replace("\n", "");
                pagesNumber = parseInt(stdout);
            }
            if (stderr != undefined && stderr != null && typeof (stderr) == "number") {
                pagesNumber = parseInt(stderr);
            }


            if (pagesNumber != undefined && pagesNumber != null && isNaN(pagesNumber) == false && pagesNumber != "") {
                if (kyoceraOldPrinterPages == null) {
                    kyoceraOldPrinterPages = pagesNumber;
                }
                tempLastKyoPrinterLages = pagesNumber;
                var pages = pagesNumber - kyoceraOldPrinterPages;
                if (isNaN(pages) == false) {
                    resolve(pages);
                } else {
                    resolve(false);
                }
                return;
            } else {
                resolve(false);
                return;
            }
            // })

        });

    });
}


async function toggleNotice() {
    var priceArea = document.getElementById("priceArea");
    var noticeArea = document.getElementById("noticeArea");
    if (priceArea != undefined && noticeArea != undefined) {
        if (priceArea.style.display == "none") {
            priceArea.style.display = "initial";
            noticeArea.style.display = "none";
        } else {
            priceArea.style.display = "none";
            noticeArea.style.display = "initial";
        }
    }
}

