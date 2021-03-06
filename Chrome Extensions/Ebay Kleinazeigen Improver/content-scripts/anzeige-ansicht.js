console.log("[EKS] Seite --> Anzeigen Ansicht");
custom_show_loading();

var button_raw_html = '<li><a href="?custom_recreate" id="viewad-action-recreate" class="button-secondary full-width taller custom-view-recreate-button"><i class="button-icon icon-redo-gray"></i><span>Anzeige Neuerstellen</span></a></li>'; 

window.addEventListener("load", windowLoaded(), false);

async function windowLoaded() {
	await addRecreateButton();
	await checkURLParams();
	custom_hide_loading();
}

async function addRecreateButton() {
	var buttons_element = document.getElementById("viewad-action-watchlist").parentElement;
	buttons_element.innerHTML = button_raw_html + buttons_element.innerHTML;
	return;
}

async function checkURLParams() {
	if (window.location.href.includes("custom_save") || window.location.href.includes("custom_recreate")) {
        console.log("Automatische Speicherung der Anzeige...");
        await storeAllData();
        if (window.location.href.includes("custom_recreate")) {
            window.location.href = "https://www.ebay-kleinanzeigen.de/p-anzeige-aufgeben-schritt2.html" + "?auto_insert=" + id;
        } else {
            window.location.href = window.location.href.replace("custom_save", "");
        }
		return;
	} else {
		return;
	}
}

async function storeAllData() {
    storeInfos();
    await downloadImages();
}

function storeInfos() {
    title = document.getElementById("viewad-title").innerHTML;
    price = document.getElementById("viewad-price").innerHTML;
    description = document.getElementById("viewad-description-text").innerHTML;
    if (document.getElementsByClassName("align-right").length > 1) {
        id = document.getElementsByClassName("align-right")[1].innerHTML;
    } else {
        id = document.getElementsByClassName("align-right")[0].innerHTML;
    }

    title = title.replace("                    ", "").replace(/(\r\n|\n|\r)/gm, "");
    price = price.replace("€", "").replace("                        ", "").replace(" ", "").replace(/(\r\n|\n|\r)/gm, "");
    description = description.replace("                        ", "").replace(/(\r\n|\n|\r)/gm, "");
    description = description.split("<br>").join("\n");
    id = id.replace("Anzeigennr.: ", "");

    localStorage.setItem(id + "_title", title);
    localStorage.setItem(id + "_price", price);
    localStorage.setItem(id + "_desc", description);
}

async function downloadImages() {
    var images = document.getElementsByClassName("galleryimage-element");
    var curr_index = 0;
    while (curr_index < images.length - 1) {
        var imgObj = images[curr_index].getElementsByTagName("img")[0];
        await storeImage(imgObj, id + "_" + (curr_index + 1) + ".jpg");
        curr_index++;
    }
	return;
}

async function storeImage(img,name) {
   forceDownload(img.src, name);
   await sleep(100);
   return;
}