console.log("Hello Mqtt Services");
var connected_flag = 0, mqtt, reconnectTimeout = 1000, host = "64.227.130.161",
    topic = "/gvd/uplink", port = 9001;
MQTTconnect();

var mqttStatus = document.querySelector(".status");


function onConnectionLost() {
    console.log("connection lost");
    connected_flag = 0;
    mqttStatus.textContent = "Disconnected";
    MQTTconnect();
}

function onFailure(message) {
    console.log("Failed");
    mqttStatus.textContent = "Disconnected";
    setTimeout(MQTTconnect(), reconnectTimeout);
}

function onMessageArrived(r_message) {
    var out_msg = r_message.payloadString;
    console.log(out_msg);
    var data = JSON.parse(out_msg);
    if (data.category === "Environment Sensor") {
        am319Parser(data);
    }

    console.log(data.name);
    //document.getElementById("data").innerHTML =data.Temperature;
    document.getElementById("data").innerHTML = out_msg;
}

function onConnected(recon, url) {
    console.log(" in onConnected " + reconn);
}

function onConnect() {
    connected_flag = 1;
    mqttStatus.textContent = "Connected";
    var mqttButton = document.getElementById("mqttButton");
    mqttButton.classList.remove("btn-outline-danger");
    mqttButton.classList.add("btn-outline-success");
    sub_topics();
}

function MQTTconnect() {
    var CID = Date();
    console.log(CID);
    console.log("connecting to " + host + " " + port);
    mqtt = new Paho.MQTT.Client(host, port, CID);
    //document.write("connecting to "+ host);
    var options = {
        timeout: 3, onSuccess: onConnect, onFailure: onFailure,
    };

    mqtt.onConnectionLost = onConnectionLost;
    mqtt.onMessageArrived = onMessageArrived;
    mqtt.onConnected = onConnected;

    mqtt.connect(options);
    return false;
}

function sub_topics() {
    console.log("Subscribing to topic =" + topic);
    mqtt.subscribe(topic);
    return false;
}

function am319Parser(data) {
    console.log("AM319 Parser");
    console.log(data);
    var am319DeviceName = data.name;
    var temperatureDataSet = document.getElementById(am319DeviceName.concat("-temperature"));
    var humidityDataSet = document.getElementById(am319DeviceName.concat("-humidity"));
    var pressureDataSet = document.getElementById(am319DeviceName.concat("-pressure"));
    var lightDataSet = document.getElementById(am319DeviceName.concat("-light"));
    temperatureDataSet.innerHTML = data.temperature + " &#8451;" ;
    humidityDataSet.innerHTML = data.humidity + " %RH";
    pressureDataSet.innerHTML = data.pressure;
    lightDataSet.innerHTML = data.light_level;
}