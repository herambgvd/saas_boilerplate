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
    var data = JSON.parse(out_msg);
    console.log(data);
    if (data.deviceName && data.deviceName.startsWith("AM319")) {
        am319Parser(data);
    }
    if (data.deviceName && data.deviceName.startsWith("VS121")) {
        vs121Parser(data);
    }
    if (data.deviceName && data.deviceName.startsWith("GS301")) { // Done
        gs301Parser(data);
    }
    if (data.deviceName && data.deviceName.startsWith("EM300")) {
        em300Parser(data);
    }
    if (data.deviceName && data.deviceName.startsWith("EM400")) {
        em400Parser(data);
    }
    if (data.deviceName && data.deviceName.startsWith("UC512")) {
        uc512Parser(data);
    }
    if (data.deviceName && data.deviceName.startsWith("WS201")) {
        ws201Parser(data);
    }

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
    console.log(data);
    var am319DeviceName = data.deviceName;
    var tvocDataSet = document.getElementById(am319DeviceName.concat("-tvoc"));
    var coDataSet = document.getElementById(am319DeviceName.concat("-co2"));
    var temperatureDataSet = document.getElementById(am319DeviceName.concat("-temperature"));
    var humidityDataSet = document.getElementById(am319DeviceName.concat("-humidity"));
    var pressureDataSet = document.getElementById(am319DeviceName.concat("-pressure"));
    var lightDataSet = document.getElementById(am319DeviceName.concat("-light"));
    var hchoDataSet = document.getElementById(am319DeviceName.concat("-hcho"));
    var pirDataSet = document.getElementById(am319DeviceName.concat("-pir"));
    var pm25DataSet = document.getElementById(am319DeviceName.concat("-pm25"));
    var pm10DataSet = document.getElementById(am319DeviceName.concat("-pm10"));
    temperatureDataSet.innerHTML = data.temperature + " &#8451;";
    humidityDataSet.innerHTML = data.humidity + "%";
    pressureDataSet.innerHTML = data.pressure + 'hPa';
    lightDataSet.innerHTML = data.light_level + "LUX";
    tvocDataSet.innerHTML = data.tvoc;
    coDataSet.innerHTML = data.co2 + "ppm";
    hchoDataSet.innerHTML = data.hcho;
    pirDataSet.innerHTML = data.pir;
    pm25DataSet.innerHTML = data.pm2_5 + 'µg/m&sup3;';
    pm10DataSet.innerHTML = data.pm10 + 'µg/m&sup3;';
}

function vs121Parser(data) {
    var vs121DeviceName = data.deviceName;
    var peopleInDataSet = document.getElementById(vs121DeviceName.concat("-people-in"));
    var peopleOutDataSet = document.getElementById(vs121DeviceName.concat("-people-out"));
    peopleInDataSet.innerHTML = data.people_in;
    peopleOutDataSet.innerHTML = data.people_out;
}

function gs301Parser(data) {
    var gs301DeviceName = data.deviceName;
    var nh3DataSet = document.getElementById(gs301DeviceName.concat("-nh3"));
    var temperatureDataSet = document.getElementById(gs301DeviceName.concat("-temperature"));
    var h2sDataSet = document.getElementById(gs301DeviceName.concat("-h2s"));
    var humidityDataSet = document.getElementById(gs301DeviceName.concat("-humidity"));
    nh3DataSet.innerHTML = data.nh3;
    temperatureDataSet.innerHTML = data.temperature + " &#8451;";
    h2sDataSet.innerHTML = data.h2s;
    humidityDataSet.innerHTML = data.humidity + "%";

}

function em300Parser(data) {
    var em300DeviceName = data.deviceName;
    var temperatureDataSet = document.getElementById(em300DeviceName.concat("-temperature"));
    var humidityDataSet = document.getElementById(em300DeviceName.concat("-humidity"));
    temperatureDataSet.innerHTML = data.temperature + " &#8451;";
    humidityDataSet.innerHTML = data.humidity + "%";
}

function em400Parser(data) {
    var em400DeviceName = data.deviceName;
    var temperatureDataSet = document.getElementById(em400DeviceName.concat("-temperature"));
    var positionDataSet = document.getElementById(em400DeviceName.concat("-position"));
    var batteryDataSet = document.getElementById(em400DeviceName.concat("-battery"));
    temperatureDataSet.innerHTML = data.temperature + " &#8451;";
    positionDataSet.innerHTML = data.position;
    batteryDataSet.innerHTML = data.battery + "%";
}

function uc512Parser(data) {
    var uc512DeviceName = data.deviceName;
    var valve1DataSet = document.getElementById(uc512DeviceName.concat("-valve_1"));
    var valve1PulseDataSet = document.getElementById(uc512DeviceName.concat("-position"));
    var valve2DataSet = document.getElementById(uc512DeviceName.concat("-valve_2"));
    var valve2PulseDataSet = document.getElementById(uc512DeviceName.concat("-valve_2_pulse"));
    valve1DataSet.innerHTML = data.temperature;
    valve1PulseDataSet.innerHTML = data.position;
    valve2DataSet.innerHTML = data.battery;
    valve2PulseDataSet.innerHTML = data.position;
}

function ws201Parser(data) {
    var ws201DeviceName = data.deviceName;
    console.log(ws201DeviceName);
    var distanceDataSet = document.getElementById(ws201DeviceName.concat("-distance"));
    var remainingDataSet = document.getElementById(ws201DeviceName.concat("-remaining"));
    distanceDataSet.innerHTML = data.distance + " cm";
    remainingDataSet.innerHTML = data.remaining + " %";
}