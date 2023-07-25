async function fetchWithTimeout(resource, options = {}) {
  const { timeout = 5000 } = options;

  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  const response = await fetch(resource, {
    ...options,
    signal: controller.signal
  });
  clearTimeout(id);

  return response;
}

async function get(url, params)
{
  const response = await fetchWithTimeout(url + '?' + new URLSearchParams(params), {
    method: 'GET', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-store',
  });
  var result;
  await response.json().then((data) => {
      if (!response.ok){
          createAlert("Ошибка: " + data.reason, 'warning');
          return;
      }
     result = data;
  });
  return result
}

async function post(url, body)
{
  const response = await fetchWithTimeout(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    cache: 'no-store',
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify(body)
  });
  var result;
  await response.json().then((data) => {
      if (!response.ok){
          createAlert("Ошибка: " + data.reason, 'warning');
          return;
      }
      result = data;
  });
  return result
}