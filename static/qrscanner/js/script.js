params = new URLSearchParams(window.location.search)
const event_el = document.querySelector('#event_id');
const event_id = params.get('event_id')
event_el.textContent = event_id

var prev_qr = '';

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

function showScanQrPopup() {
    Telegram.WebApp.showScanQrPopup({
        text: 'Scan personal QR code'
    }, function(text) {
        if(prev_qr !== text) {
            prev_qr = text;
            apiRequest('scanned', {qr_data: text, event_id: event_id}, function (result) {
                if (result && result.user_id) {
                    Telegram.WebApp.showAlert(`Вы отметили пользователя. 
                    Пользователь: ${result.first_name} ${result.last_name}.
                    ID: ${result.user_id}`);
                } else if (result.reason) {
                    Telegram.WebApp.showAlert(result.reason);
                }

            })
        }
    });
}
Telegram.WebApp.ready();
Telegram.WebApp.MainButton.setParams({
    text: 'CLOSE',
    is_visible: true
}).onClick(Telegram.WebApp.close);


checkInitData();