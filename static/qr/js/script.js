function apiRequest(method, data, onCallback) {
    const authData = Telegram.WebApp.initData || '';
    fetch('/bot/api/' + method, {
        method: 'POST',
        body: JSON.stringify(Object.assign(data, {
            auth: authData,
        })),
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(response) {
        return response.json();
    }).then(function(result) {
        onCallback && onCallback(result);
    }).catch(function(error) {
        alert(error)
        onCallback && onCallback({error: 'Server error'});
    });
}

function showQR(qr_data){
    const qrCode = new QRCodeStyling({
        width: 250,
        height: 250,
        type: "svg",
        data: qr_data,
        image: "{% static 'qr/images/unlock_logo1.svg' %}",
        dotsOptions: {
            color: "#000000",
            type: "rounded"
        },
        margin: 5,
        backgroundOptions: {
            color: "#e9ebee",
        },
        imageOptions: {
            crossOrigin: "anonymous",
            margin: 1,
            imageSize: 0.35
        }
    });
    canvas = document.getElementById("qr_code")
    qrCode.append(canvas);
    canvas.children.item(0).classList.add("round");
}

function checkInitData() {
    const webViewStatus = document.querySelector('#webview_data_status');
    const user_name = document.querySelector('#user_name');
    const user_username = document.querySelector('#user_username');
    const version = document.querySelector('#ver');
    const platform = document.querySelector('#platform');
    if (Telegram.WebApp.initDataUnsafe.query_id &&
    Telegram.WebApp.initData &&
        webViewStatus.classList.contains('status_need')
    ) {

        webViewStatus.classList.remove('status_need');
        apiRequest('checkinitdata', {}, function(result) {
            if (result.valid) {
                webViewStatus.textContent = 'Hash is correct (async)';
                webViewStatus.className = 'ok';
                user_name.textContent = Telegram.WebApp.initDataUnsafe.user.first_name
                user_username.textContent = Telegram.WebApp.initDataUnsafe.user.username
                version.textContent = Telegram.WebApp.version
                platform.textContent = Telegram.WebApp.platform
            } else {
                webViewStatus.textContent = result.error + ' (async)';
                webViewStatus.className = 'err';
            }
        });
    }
}

checkInitData();

apiRequest("qr", {}, function(result) {
    showQR(result.qr_data);
});
