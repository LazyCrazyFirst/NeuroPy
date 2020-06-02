// Подключиться к веб-сокету
var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

// Создаем распознаватель
var recognizer = new webkitSpeechRecognition();

//считывание без остоновки
//recognizer.continuous = true;

// Ставим опцию, чтобы распознавание началось ещё до того, как пользователь закончит говорить
recognizer.interimResults = true;

// Какой язык будем распознавать?
recognizer.lang = 'ru-Ru';

//Задаём переменную для вывода того, что мы сказали
var textElement = document.querySelector('.input');

//Для голоса Анечки
var synth = window.speechSynthesis;

//Для кнопки вкл/выкл
var toggle = 0;

//Для определени того, что пользователь ничего не сказал
var nice = 0;

// присваиваем значения для того, чтобы Анечка не повторяла несколько раз ответ
var k = document.querySelector('.text').textContent;

var l = 0;

//Если голос уловлен
recognizer.onresult = function (event) {
    //Присваиваем переменной значение 1, т.к после прослушивания микрофон выключится и если
    //пользователь ничего не сказал, сработает условие в функции recognizer.onend, чтобы распознование не выключилось
    nice = 1;
    var result = event.results[event.resultIndex];
    //если пользователь закончил говорить
    if (result.isFinal) {
        //элементу HTML присваивается значение
        textElement.textContent = "Вы сказали: " + result[0].transcript;
        //передаём конечное значение на сервер в python, для дальнейшей обработки
        var selection = result[0].transcript;
        socket.emit('submit vote', {'selection': selection});

        //запускаем функции озвучивания ответа
        talk();
    }
}

//После прослушивания микрофон выключится и если пользователь ничего не сказал,
//сработает условие в функции, чтобы распознование не выключилось
recognizer.onend = function () {
    if ((nice === 0) && (toggle === 1)) {
        document.querySelector('.text').textContent = "Ничего не слышу";
        k = "kkk";
        talk();
    }
}

//МОЖНО ВЫКЛЮЧИТЬ ТОЛЬКО КОГДА ИДЁТ РАСПОЗНОВАНИЕ ГОЛОСА!!!!!!!
function stop() {
    if (synth.speaking === false) {
        recognizer.abort();
    }
}


function wait() {
    //включаем таймер
    interval = setInterval(function () {
        //если закончил говорить
        if (synth.speaking === false) {
            //останавливаем таймер
            clearInterval(interval);
            nice = 0;
            //запускаем функцию распознования речи
            speech();
        }
    }, 500);
}

function speech() {
// Начинаем слушать микрофон и распознавать голос
    recognizer.start();
}

//функция проговаривания результата
function talk() {
    //создаём таймер
    interval = setInterval(function () {
        //присваиваем переменной значение текстового поля
        text = document.querySelector('.text').textContent;
        l += 1;
        console.log("text "+text);
        console.log("k "+k);
        //если оно не одно и тоже, что и было на предыдущем шаге, то
        if (text != k) {
            //останавливаем таймер
            clearInterval(interval);
            k = text;
            l = 0;
            //озвучиваем результат
            text = text.replace("Анечка: ", "")
            var utterance = new SpeechSynthesisUtterance(text);
            synth.speak(utterance);
            //для перехода по транице
            if ((text === "Дом") || (text === "Информация") || (text === "Преимущества") || (text === "Команда") || (text === "Способности") || (text === "Контакты")){
                switch (text) {
                    case "Дом":
                        $('#home_drag').trigger('click');
                        break;
                    case "Информация":
                        $('#about_drag').trigger('click');
                        break;
                    case "Преимущества":
                        $('#advantages_drag').trigger('click');
                        break;
                    case "Команда":
                        $('#team_drag').trigger('click');
                        break;
                    case "Способности":
                        $('#abilities_drag').trigger('click');
                        break;
                    case "Контакты":
                        $('#contact_drag').trigger('click');
                        break;
                    default:
                        alert("Ошибочка)))");

                }
            }
            if (text !== "Молчу"){
                //функция "подождать пока говорит"
                wait();
            }
            else {
                $('#krestik').trigger('click');
            }


        }
        //чтобы не случилось зацикливание
        //или когда 2 раза вызывают одно и тоже
        if (l > 7) {
            //останавливаем таймер
            clearInterval(interval);
            //говорит, что не попугай
            document.querySelector('.text').textContent = "Я не попугай"
            var utterance = new SpeechSynthesisUtterance("Я не попугай");
            synth.speak(utterance);
            wait();
            l = 0;
        }

    }, 500)


}

//Первое нажатие по кнопке - включение, второе - выключение
function toggler() {
    if (toggle === 0) {
        speech();
        toggle = 1;
    } else {
        stop();
        toggle = 0;
    }

}


