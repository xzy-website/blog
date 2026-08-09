console.log('✅ butterfly-clock-hexo.js 已加载');

function clockUpdateTime(info, city) {
  if (!city) city = '长沙市';

  let currentColor = '#000';
  switch (info.now.icon) {
    case '100': currentColor = '#fdcc45'; break;
    case '101': currentColor = '#fe6976'; break;
    case '102':
    case '103': currentColor = '#fe7f5b'; break;
    case '104':
    case '150':
    case '151':
    case '152':
    case '153':
    case '154':
    case '800':
    case '801':
    case '802':
    case '803':
    case '804':
    case '805':
    case '806':
    case '807': currentColor = '#2152d1'; break;
    case '300':
    case '301':
    case '305':
    case '306':
    case '307':
    case '308':
    case '309':
    case '310':
    case '311':
    case '312':
    case '313':
    case '314':
    case '315':
    case '316':
    case '317':
    case '318':
    case '350':
    case '351':
    case '399': currentColor = '#49b1f5'; break;
    case '302':
    case '303':
    case '304': currentColor = '#fdcc46'; break;
    case '400':
    case '401':
    case '402':
    case '403':
    case '404':
    case '405':
    case '406':
    case '407':
    case '408':
    case '409':
    case '410':
    case '456':
    case '457':
    case '499': currentColor = '#a3c2dc'; break;
    case '500':
    case '501':
    case '502':
    case '503':
    case '504':
    case '507':
    case '508':
    case '509':
    case '510':
    case '511':
    case '512':
    case '513':
    case '514':
    case '515': currentColor = '#97acba'; break;
    case '900':
    case '999': currentColor = 'red'; break;
    case '901': currentColor = '#179fff;'; break;
    default: break;
  }

  var clock_box = document.getElementById('hexo_electric_clock');
  if (!clock_box) {
    console.warn('[渲染] 未找到 #hexo_electric_clock');
    return;
  }

  clock_box.innerHTML = `
  <div class="clock-row">
    <span id="card-clock-clockdate" class="card-clock-clockdate"></span>
    <span class="card-clock-weather"><i class="qi-${info.now.icon}-fill" style="color: ${currentColor}"></i> ${info.now.text} <span>${info.now.temp}</span> ℃</span>
    <span class="card-clock-humidity">💧 ${info.now.humidity}%</span>
  </div>
  <div class="clock-row">
    <span id="card-clock-time" class="card-clock-time"></span>
  </div>
  <div class="clock-row">
    <span class="card-clock-windDir"> <i class="qi-gale"></i> ${info.now.windDir}</span>
    <span class="card-clock-location">${city}</span>
    <span id="card-clock-dackorlight" class="card-clock-dackorlight"></span>
  </div>
  `;

  var week = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];
  var loading = document.getElementById('card-clock-loading');
  if (loading) loading.innerHTML = '';

  function updateTime() {
    var cd = new Date();
    var h = zeroPadding(cd.getHours(), 2);
    var m = zeroPadding(cd.getMinutes(), 2);
    var s = zeroPadding(cd.getSeconds(), 2);
    var d = zeroPadding(cd.getFullYear(), 4) + '-' +
            zeroPadding(cd.getMonth()+1, 2) + '-' +
            zeroPadding(cd.getDate(), 2) + ' ' +
            week[cd.getDay()];
    var ampm = cd.getHours() >= 12 ? ' P M' : ' A M';

    var timeDom = document.getElementById('card-clock-time');
    var dateDom = document.getElementById('card-clock-clockdate');
    var ampmDom = document.getElementById('card-clock-dackorlight');
    if (timeDom) timeDom.innerHTML = h + ':' + m + ':' + s;
    if (dateDom) dateDom.innerHTML = d;
    if (ampmDom) ampmDom.innerHTML = ampm;
  }

  function zeroPadding(num, digit) {
    var zero = '';
    for (var i = 0; i < digit; i++) zero += '0';
    return (zero + num).slice(-digit);
  }

  setInterval(updateTime, 1000);
  updateTime();
}

function getIpInfo() {
  if (!localStorage.getItem('clock_location_alert_shown')) {
    alert('请允许浏览器访问您的位置，否则侧边栏时钟将无法获取您的城市和天气信息。');
    localStorage.setItem('clock_location_alert_shown', 'true');
  }

  console.log('🚀 [主流程] 开始执行定位与天气获取');

  var DEFAULT_CITY = '长沙市';
  var DEFAULT_LOCATION = (typeof clock_rectangle !== 'undefined') ? clock_rectangle : '113.0,28.2';

  if (typeof qweather_key === 'undefined' || !qweather_key) {
    console.error('❌ qweather_key 未定义');
    return;
  }
  if (typeof gaud_map_key === 'undefined' || !gaud_map_key) {
    console.warn('⚠️ gaud_map_key 未定义，将无法获取城市名，但天气仍会显示');
  }

  function fetchWeatherAndRender(location, city) {
    var finalCity = city || DEFAULT_CITY;
    var weatherUrl = 'https://pj3yfueptd.re.qweatherapi.com/v7/weather/now?location=' +
                      encodeURIComponent(location) + '&key=' + qweather_key;
    console.log('[天气] 请求 URL:', weatherUrl);

    fetch(weatherUrl)
      .then(function(res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.json();
      })
      .then(function(data) {
        console.log('[天气] 返回数据:', data);
        if (data.code === '200') {
          if (!city && data.location) {
            finalCity = data.location;
          }
          if (document.getElementById('hexo_electric_clock')) {
            clockUpdateTime(data, finalCity);
          }
        } else {
          console.error('[天气] API 错误:', data.code, data.msg || '');
          var fallbackUrl = 'https://pj3yfueptd.re.qweatherapi.com/v7/weather/now?location=' +
                             DEFAULT_LOCATION + '&key=' + qweather_key;
          fetch(fallbackUrl)
            .then(function(r) { return r.json(); })
            .then(function(fbData) {
              if (document.getElementById('hexo_electric_clock')) {
                clockUpdateTime(fbData, DEFAULT_CITY);
              }
            });
        }
      })
      .catch(function(err) {
        console.error('[天气] 网络请求失败:', err);
        var fallbackUrl = 'https://pj3yfueptd.re.qweatherapi.com/v7/weather/now?location=' +
                           DEFAULT_LOCATION + '&key=' + qweather_key;
        fetch(fallbackUrl)
          .then(function(r) { return r.json(); })
          .then(function(fbData) {
            if (document.getElementById('hexo_electric_clock')) {
              clockUpdateTime(fbData, DEFAULT_CITY);
            }
          });
      });
  }

  if (!navigator.geolocation) {
    console.warn('[定位] 浏览器不支持 Geolocation API');
    fetchWeatherAndRender(DEFAULT_LOCATION, DEFAULT_CITY);
    return;
  }

  console.log('[定位] 尝试请求浏览器位置权限...');
  navigator.geolocation.getCurrentPosition(
    function(pos) {
      var lat = pos.coords.latitude;
      var lng = pos.coords.longitude;
      var location = lng + ',' + lat;
      console.log('[定位] 获取到坐标:', location);

      if (gaud_map_key) {
        var geoUrl = 'https://restapi.amap.com/v3/geocode/regeo?key=' + gaud_map_key +
                      '&location=' + location + '&output=json';
        console.log('[定位] 请求高德逆地理:', geoUrl);

        var script = document.createElement('script');
        var callbackName = 'amap_callback_' + Date.now();
        window[callbackName] = function(data) {
          delete window[callbackName];
          document.body.removeChild(script);
          if (data.status === '1' && data.regeocode) {
            var addr = data.regeocode.addressComponent;
            var city = addr.city || addr.province || DEFAULT_CITY;
            console.log('[定位] 高德解析城市:', city);
            fetchWeatherAndRender(location, city);
          } else {
            console.warn('[定位] 高德逆地理失败');
            fetchWeatherAndRender(location, null);
          }
        };
        script.src = geoUrl + '&callback=' + callbackName;
        script.onerror = function() {
          console.warn('[定位] 高德 JSONP 请求失败');
          fetchWeatherAndRender(location, null);
        };
        document.body.appendChild(script);
      } else {
        fetchWeatherAndRender(location, null);
      }
    },
    function(err) {
      console.warn('[定位] 浏览器定位失败 (' + err.code + '):', err.message);
      fetchWeatherAndRender(DEFAULT_LOCATION, DEFAULT_CITY);
    },
    { timeout: 8000, enableHighAccuracy: false }
  );
}

if (typeof qweather_key === 'undefined' || !qweather_key) {
  console.error('❌ 启动失败：qweather_key 未定义');
} else {
  getIpInfo();
}