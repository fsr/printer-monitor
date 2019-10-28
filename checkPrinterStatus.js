
var e = require('child_process');
var dellOldPrinterPages = null;
var dellCommand = "snmpget -v2c -O vq -c public 192.168.1.10 SNMPv2-SMI::mib-2.43.10.2.1.4.1.1";

function setPrice(price = "ERROR") {
    if(typeof(price)=="number"){
        price = (Math.ceil(price*20)/20).toFixed(2);
        var priceString = price.toString();
        var priceParts =  priceString.split(".");
        if(priceParts.length>1){
            if(priceParts[1].length==1){
                priceString+="0";
            }
        }
        if(priceParts.length==1){
            priceString+=",00";
        }
        priceString.replace(".",",");
        priceString+="€";
        var priceElement = document.getElementById("price");
        if (priceElement != undefined) {
            priceElement.innerHTML = priceString;
        }
    }
}

function setPages(pages){
    if(pages!=undefined&& pages!=null){
        var pagesElement = document.getElementById("pages");
        if (pagesElement != undefined) {
            pagesElement.innerHTML = pages;
        }
    }
}

async function setup() {
    reset();
    setInterval(() => {
        toggleNotice();
        updateData();
    }, 5000);
}
setup();

function reset() {
        e.exec(dellCommand, function (err, stdout, stderr) {
            var pagesNumber = null;
            if(stdout!=undefined&& stdout!=null){
                stdout = stdout.replace("\n","");
                pagesNumber = parseInt(stdout);
            }
            if(stderr!=undefined&& stderr!=null && typeof(stderr)=="number"){
                pagesNumber = parseInt(stderr);
            }
            if(pagesNumber!=undefined && pagesNumber!=null){
                dellOldPrinterPages = pagesNumber;
            } else {
               console.log("error resetting"); 
            }
            
        });
        setPrice(0);
        setPages(0);
    
}

async function updateData() {
    console.log("update");
    try {
        var pages = await getDellData();
        console.log(pages);
        if(pages!=undefined && pages!=null &&pages!=false){
            setPages(pages);
            var price = pages * 0.02;
            setPrice(price);
        }
    } catch (e) {
        console.log("error getting pages");
    }

}

async function getDellData() {
    return new Promise((resolve, reject) => {
        e.exec(dellCommand, function (err, stdout, stderr) {
            var pagesNumber = null;
            
            if(stdout!=undefined&& stdout!=null){
                stdout = stdout.replace("\n","");
                pagesNumber = parseInt(stdout);
            }
            if(stderr!=undefined&& stderr!=null && typeof(stderr)=="number"){
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

