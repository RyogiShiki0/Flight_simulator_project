
document.getElementById('usernameForm').addEventListener('submit', function (e) {
    e.preventDefault(); // 防止表单默认提交刷新页面

    const username = document.getElementById('username').value;
    const messageElement = document.getElementById('message');

    // 发送 AJAX 请求到后端
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ username })
    })
    .then(response => response.json())
    .then(data => {
        // 根据后端返回的结果更新页面
        if (data.exists) {
            messageElement.textContent = data.message;
            messageElement.style.color = 'red';
        } else {
            document.getElementById("country-menu").style.display="block"
            document.getElementById("welcome").style.display="none"
        }
    })
    .catch(error => {
        console.error('Error:', error);
        messageElement.textContent = 'An error occurred. Please try again later.';
        messageElement.style.color = 'red';
    });
});

document.querySelectorAll('.country-select-menu-button').forEach(button => {
    button.addEventListener('click', function (event) {
        event.preventDefault();

        const country = this.getAttribute('data-country');
        const resultMessage = document.getElementById('resultMessage');
        const airportMenu = document.getElementById('airport-menu');
        const airportList = document.getElementById('airport-list');

        airportMenu.style.display = 'none';
        airportList.innerHTML = ''; // 清空列表
        resultMessage.textContent = '';

        fetch('/submit_country', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ country })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                resultMessage.textContent = `Airports in ${country}:`;
                resultMessage.style.color = 'green';

                // 显示机场列表并添加按钮
                data.airports.forEach(airport => {
                    const listItem = document.createElement('li');
                    listItem.textContent = airport;

                    // 创建选择按钮
                    const selectButton = document.createElement('button');
                    selectButton.textContent = "Select";
                    selectButton.addEventListener('click', function () {
                        selectAirport(airport);
                    });

                    listItem.appendChild(selectButton);
                    airportList.appendChild(listItem);
                });

                airportMenu.style.display = 'block';
            } else {
                resultMessage.textContent = data.message;
                resultMessage.style.color = 'red';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultMessage.textContent = 'An error occurred. Please try again.';
            resultMessage.style.color = 'red';
        });
    });
});

function selectAirport(airport) {
    fetch('/select_airport', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({ airport })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("side-bar-money").innerHTML = data.money
        document.getElementById("side-bar-point").innerHTML = data.fuel
        document.getElementById("side-bar-location").innerHTML = data.airport
        document.getElementById("country-menu").style.display = "none"
        document.getElementById("airport-menu").style.display = "none"
        document.getElementById("main-select-menu").style.display = "block"
        document.getElementById("side-bar-username").innerHTML = data.username
        init(data.latitude,data.longitude);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}



function loadGoods() {
    fetch('/get_goods', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const goodsList = document.querySelector('.goods-list');
            goodsList.innerHTML = ''; // 清空列表
            console.log(data.goods)
            data.goods.forEach(item => {
                const itemDiv = document.createElement('div');
                itemDiv.innerHTML = `
                    <p>${item.goods_name} - Weight: ${item.goods_weight}, Value: ${item.goods_value}</p>
                    <button onclick="buyItem(${item.goods_ID})">Buy</button>
                `;
                goodsList.appendChild(itemDiv);
            });
        }
    });
}
function buyItem(goodsId) {
    console.log(goodsId)
    fetch('/buy_item', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ goods_id: goodsId, quantity: 1 })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById("side-bar-money").innerHTML = data.money
        if (data.success) {
            loadGoods(); // 重新加载物品
        }
    });
}
function startFlight() {
    fetch('/start_flight', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ total_value: 1000 }) // 示例总价值
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            // 可以跳转到下一步
        }
    });
}
function startTransportMission() {
    document.getElementById('main-select-menu').style.display = 'none';
    document.getElementById('item-select-menu').style.display = 'block';
    loadGoods();
}