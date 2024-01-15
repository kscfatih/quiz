      



        function sertifikaS(){
            var csrfToken = getCookie('csrftoken');
            var dataToSend = {
                isim: $('input[name="quiz_attr_1"]').val() 
            };
            console.log("isimmm : ", dataToSend);
        
            console.log("csrf tokenbnn  : ", csrfToken);
                $.ajax({
                    type: 'POST',
                    url: '/panel/sertifika/',  
                    data: dataToSend,
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    success: function(response) {
                        window.open(response.url, '_blank');
                    },
                    error: function(error) {
                        console.log("Hata oluştu:", error);
                    }
                });
        }
        
            var a=0;
        function stepbarcreate(sayi) {
            var spanElement = document.querySelector(".soru-sayisi-sol");
            if(a==0){
            a=1;
            spanElement.innerHTML = sayi;
            }
            
            console.log("sayı2:",sayi);
            container2 = $("#stepbar");
            let template = `
            <div class="bar">
                <div class="w-100 fill"></div>
            </div>
                `;
             for(let i = 1; i <= sayi; i++) {
                console.log("step eklendi");
                container2.append(template);
            }
        }
        function checkImageSrc() {
            $('.answer-image').each(function() {
                var srcValue = $(this).attr('src');
                if (!srcValue || srcValue.trim() === 'null' || srcValue === 'undefined') {
                    $(this).css('display', 'none');
                }
            });
        }
        var b=0;
        function onAjaxSuccess(response,sorular,cevaplar) {
            $('.questions-card').show();
            console.log(cevaplar);
            console.log(sorular);
            var divs = $('.section-container section');
            divs.hide().first().show(); 
            let numberOfSteps = response;
            let container = $("#show-section");
            console.log("sayı:",response);
            if(b==0){
                b=1;
                var c=0;
                h = 0;
        
                for(let i = 1; i <= response; i++) {
                    
                soru = sorular[h];
                data=soru.fields.question;
                data = data.replace(/\\/g, ""); 
                soru.fields.question = data;
                console.log("güncellenen soru : ",data)
                console.log("fonksiyon çalıştı : ",soru.fields.question);
                let template = `
                    <section class="steps">
                        <div id="step${i}" >
                            <div class="q-heading">
                                ${data} 
                            </div>
                            <div class="form-inner mt-5">
                                <div class="answer-container" >`;
                                var k = 0;
                                let letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']; 
                                let l = 0;  
                                for (let j = 0; j < cevaplar.length; j++) {
                                    cevap = cevaplar[j];
                                    if (cevap.fields.question == soru.pk) {
                                        template += `
                                    
                                            <div class="delay-${k}00 bounce-left radio-field">
                                                <span class="answer-letter" style="font-weight:bold;">${letters[l]})</span>
                                                <input class="checkmark answer-btna " style="background-color:transparent; cursor: pointer;  width:100%;"  type="radio" name="op${i}" value="${cevap.fields.correct}"/>
                                                <img class="answer-image imgas" onclick="showImageInModal(this)" src="${cevap.fields.image}" />
                                                <label style="z-index: -1;" class="ans-yazi op${k}">${cevap.fields.answer}</label>
                                            </div>
                                        `;
                                        k = k + 1;
                                        l = l + 1;  
                                    }
                                }
                                if(i<sorular.length){
                                    console.log("i : ",i)
                                    console.log("soruların uzunluğu : ",sorular.length)
                                    template += `
                                
                                            </div>
                                        </div>
                                            <div class="next-prev">
                                                <button class="prev mt-2 gerii"  style="background-color:#e9434e; color:#f8f9fa;" type="button" >
                                                    Geri
                                                </button>
        
                                                <button type="button"   data-id="${i}" class="nextt next step-btn next-btnn" id="step${i}btn">
                                                    İleri
                                                </button>
                                            
        
                                            </div>
                                        </div>  
                                    </section>
                        `;} else {
                            console.log("sub eklendi");
                            template += `
                                    </div>
                                </div>
                                    <div class="next-prev">
                                        <button class="prev mt-2 "style=" background-color:#e9434e; color:#f8f9fa;" type="button">
                                            Geri
                                        </button> 
                                    
                                    
                                        <button type="button " data-id="${i}" class="next nextt step-btn next-btnn" id="sub">
                                            İleri
                                        </button>
        
                                    </div>
                                </div>
                            </section>
                        `;
            
        }
        
            
                    container.append(template);
                    h++;
                    checkImageSrc();
                }
                var divs = $('.section-container section');
                    divs.hide().first().show(); 
                }
              
                
        }
        
        
        
        function checkScreenWidth() {
            var width = $(window).width();
            var $container = $('.next-prev');
            var $geriBtn = $('.gerii');
            
            if (width <= 768) {
            
                $container.append($geriBtn);
            } else {
             
                $container.prepend($geriBtn);
            }
        }
        
        
        
        function transformContent(content) {    
            
            const audioWavRegex = /\[audio wav="(.*?)"\]\[\/audio\]/g;
            content = content.replace(audioWavRegex, '<audio controls><source src="$1" type="audio/wav">Tarayıcınız ses etiketini desteklemiyor.</audio>');
        
            const audioMp3Regex = /\[audio mp3="(.*?)"\]\[\/audio\]/g;
            content = content.replace(audioMp3Regex, '<audio controls><source src="$1" type="audio/mpeg">Tarayıcınız ses etiketini desteklemiyor.</audio>');
        
            const videoRegex = /\[video width="(\d+)" height="(\d+)" m4v="(.*?)"\]\[\/video\]/g;
            content = content.replace(videoRegex, '<video class="responsive-video" width="400" height="400" controls><source src="$3" type="video/mp4">Tarayıcınız video etiketini desteklemiyor.</video>');
        
            const videoRegexa = /\[video width="(\d+)" height="(\d+)" mp4="(.*?)"\]\[\/video\]/g;
            content = content.replace(videoRegexa, '<video class="responsive-video" width="400" height="400" controls><source src="$3" type="video/mp4">Tarayıcınız video etiketini desteklemiyor.</video>');
        
            return content;
        }
        
        
        
        function transferContent() {
            if (window.innerWidth <= 1350) {
                var sideImgDiva = document.querySelector('.side-img2');
                var spanss = document.querySelector('.spanss');
                sideImgDiva.style.display = 'none';
                spanss.style.display = 'none';
                return;
            }
            var spansss = document.querySelector('.spanss');
            spansss.style.display = 'block';
            var stepSections = document.querySelectorAll('.steps');
            for (let section of stepSections) {
                if (getComputedStyle(section).display !== 'none') {
                    var qHeadingDiv = section.querySelector('.q-heading');
                    var sideImgDiv = document.querySelector('.side-img2');
                   
                    if (qHeadingDiv && sideImgDiv) {
                        sideImgDiv.innerHTML = qHeadingDiv.innerHTML;
                    
                        sideImgDiv.innerHTML = transformContent(sideImgDiv.innerHTML);
                 
            
                        qHeadingDiv.style.display = 'none';
                    } else {
                        console.error("Beklenen div'ler bulunamadı.");
                    }
        
                    break;
                }
            }
        }
        
        
        
        function updateOnlineUsers() {
                    fetch('/panel/update_user/')
                        .then(response => response.json())
                        .then(data => {
                        
                        });
                }
            
                function fetchOnlineUsers() {
                    fetch('/panel/get_online_users/')
                        .then(response => response.json())
                        .then(data => {
                        
                        });
                }
                setInterval(updateOnlineUsers, 1000);
                setInterval(fetchOnlineUsers, 1000);
        
        
            
        var now = 0; 
        
        function showActiveStep(soru_adedi)    {
            var visibleStep = null;
            for (var i = 1; i <= soru_adedi; i++) { 
                if ($('#step' + i).is(':visible')) {
                    visibleStep = i;
                    break;
                }
            }
            if (visibleStep !== null) {
                $(".step-bar .bar .fill").eq(now).addClass('w-100');
                $("#activeStep").html(visibleStep);
                $("#activeStep2").html(visibleStep);
                console.log("step değiştirildi",visibleStep)
            } else {
                console.log("error");
            }
        }
        
        
        function next(soru_adedi,selector)
        {
            var divs = $(selector);
            console.log("section sayısı : ",divs.length);
            console.log("next çaloıştı");
            divs.eq(now).hide();
            now = (now + 1 < divs.length) ? now + 1 : 0;
            divs.eq(now).show(); 
            console.log(now);
            transferContent();
            showActiveStep(soru_adedi);
            return now;
        }
        
        
        var checkedradio = false;
        
        function radiovalidate(stepnumber)
        {
            console.log("radio validate çalıştı",stepnumber);
            var checkradio = $("#step"+stepnumber+" input").map(function()
            {
            if($(this).is(':checked'))
            {
                return true;
            }
            else
            {
                return false;
            }
            }).get();
        
            checkedradio = checkradio.some(Boolean);
        }
        
        function getCookie(name) {
                let value = "; " + document.cookie;
                let parts = value.split("; " + name + "=");
                if (parts.length == 2) return parts.pop().split(";").shift();
        }
           
        function setCookie(name, value, seconds) {
            let expires = "";
            if (seconds) {
                let date = new Date();
                date.setTime(date.getTime() + (seconds * 1000)); 
                expires = "; expires=" + date.toUTCString();
            }
            document.cookie = name + "=" + (value || "") + expires + "; path=/";
        }
        
        function zaman_takip(time){
            console.log(time);
            const timerDiv = document.getElementById('timer');
            const endMessage = document.getElementById('endMessage');
            const gecen_sure = document.getElementById('gecen_sure');
            let sure = 0;
            let timeLeft = time;
            let countdown;
                timerDiv.textContent = timeLeft;
            
                countdown = setInterval(function() {
                    timeLeft--;
                    sure++;
                    timerDiv.textContent = timeLeft;
                    
                    gecen_sure.value=sure;
                    if (timeLeft <= 0) {
                        clearInterval(countdown);
                        timerDiv.style.display = 'none';
                        endMessage.style.display = 'block';
                    }
                }, 1000);
            
        }
        
        function handleRadioChange(radioInput) {
        
            let name = radioInput.name;
            let radios = document.querySelectorAll(`input[type="radio"][name="${name}"]`);
            if (radioInput.value === "1") {
                playAudio('https://www.quizvar.com/wp-content/uploads/2021/06/nice-new.wav');
            } else if (radioInput.value === "0") {
                playAudio('https://www.quizvar.com/wp-content/uploads/2022/01/wrong.mp3');
            }
        
            if (radioInput.value === "1") {
                radioInput.style.border = "2px solid green";
                let wrongImage = document.createElement('img');
                    wrongImage.src = 'https://quizvar.com/medya_dosyalari/correct-style-9.png';  // Buraya doğru resim yolunu ekleyin
                    wrongImage.className = 'animated-image-A';
                    wrongImage.alt = 'Wrong Selection';
                            
                    let currentImage = radioInput.parentElement.querySelector('img');
        
                    if (currentImage) {  
        
                        let wrapperDiv = document.createElement('div');
                        wrapperDiv.className = 'image-wrapper'; 
                    
                        wrapperDiv.appendChild(wrongImage);
                        currentImage.insertAdjacentElement('afterend', wrapperDiv);
                    } else {
                        radioInput.parentElement.appendChild(wrongImage);
                    }
            }else{
                    radioInput.parentElement.className = radioInput.parentElement.className.replace(/\bcheckmark\b/g, "");
                    radioInput.classList.remove('checkmark');
                    radioInput.style.border = "2px solid red";
                    let wrongImage = document.createElement('img');
                    wrongImage.src = 'https://quizvar.com/medya_dosyalari/wrong-style-9.png'; 
                    wrongImage.className = 'animated-image-A';
                    wrongImage.alt = 'Wrong Selection';
                    let currentImage = radioInput.parentElement.querySelector('img');
        
                    if (currentImage) {  
                        let wrapperDiv = document.createElement('div');
                        wrapperDiv.className = 'image-wrapper'; 
                        wrapperDiv.appendChild(wrongImage);
                        currentImage.insertAdjacentElement('afterend', wrapperDiv);
                    } else {
                        radioInput.parentElement.appendChild(wrongImage);
                    }
            }
            radios.forEach(function(radio) {
                radio.disabled = true;
            });
        }
        
        function playAudio(url) {
            let audio = new Audio(url);
            audio.play();
        }
        
        function getsCookie(name) {
                let value = "; " + document.cookie;
                let parts = value.split("; " + name + "=");
                if (parts.length == 2) return parts.pop().split(";").shift();
        }
        
        function puan_hesapla(soru_adedi,interval,option){
            const quizInput = document.getElementById('quiz_id');
            document.cookie = "lastQuizTaken=" + quizInput.value;
            var totalPoints = 100;
            var totalQuestions = soru_adedi;
            var pointsPerQuestion = totalPoints / totalQuestions;
            var earnedPoints = 0;
            var dogrular = 0;
            var yanlislar = 0;
            var radioInputs = document.querySelectorAll("input[type='radio']:checked");
            console.log("interval : ",interval);
            radioInputs.forEach(function(input) {
                if (input.value === "1") {
                    dogrular += 1;
                    earnedPoints += pointsPerQuestion;
                    earnedPoints = parseFloat(earnedPoints.toFixed(2));
                    if(dogrular == soru_adedi){
                        earnedPoints = 100;
                    }
                }else{
                    yanlislar += 1;
                }
            });
            eksi_puan = 100-earnedPoints;
            var form_baslik = option.rate_form_title;pass_check 
            var resultDiv = document.querySelector('.result_msg'); 
            var sertifika= document.querySelector('.sertifika'); 
            var result_show2 = document.querySelector('.result_show2');
            var dogru_puan = document.querySelector('.dogru_puan');
            var testi_gecti = document.querySelector('.testi_gecti');
            var pass_check = document.querySelector('.pass_check');
            var dogru_sayisi = document.getElementById('dogru_sayisi');
            var yanlis_sayisi = document.getElementById('yanlis_sayisi');
            var dogru_puan_ = document.getElementById('dogru_puan_');
            var mobil_puan = document.querySelector('.mobil-puan');
            dogru_sayisi.value = dogrular;
            yanlis_sayisi.value = yanlislar;
            result_show2.innerHTML = form_baslik;
            dogru_puan_.value = earnedPoints;
            dogru_puan.innerHTML = earnedPoints;
            testi_gecen_mesaj = option.pass_score_message;
            mobil_puan.innerHTML = earnedPoints;
            console.log(option.pass_score,earnedPoints,interval);
            if(interval.length != 0){
            for(let i=0; i<interval.length; i++){
                interval_ = interval[i];
                var icerik =  interval_.interval_text;
                var gif = interval_.interval_image;
                const divElement = document.querySelector('.result_msg');
        
                if(interval_.interval_min <= earnedPoints && interval_.interval_max>= earnedPoints){
                    if(sertifika){
                    sertifika.style.display = 'none'
                        }    
                    if (resultDiv) {
                        resultDiv.innerHTML = icerik;
                    }
                    if(option.pass_score <= earnedPoints || option.pass_score == earnedPoints){
                        if(sertifika){
                    sertifika.style.display = 'block'
                        }    
                  
                        pass_check.style.cursor = 'pointer';
                    
                        testi_gecti.innerHTML = testi_gecen_mesaj;
                    }else{
                        if(sertifika){
                    sertifika.style.display = 'none'
                        }    
                    }
                       
                    if (divElement && gif && gif !== "none") {
                        const imgElement = document.createElement('img');
                        imgElement.src = gif;
                        imgElement.width = 150;
                                
                        divElement.appendChild(imgElement);
                    }
                }
            }
            }else if(interval.length == 0){
                console.log("interval 0");
                if(option.pass_score <= earnedPoints || option.pass_score == earnedPoints){
                    sertifika.style.display = 'block'
                    pass_check.style.cursor = 'pointer';
                    testi_gecti.innerHTML = testi_gecen_mesaj;
                }
            }
        
        }
        
        function shuffleArray(array) {
            let shuffled = array.slice(); 
        
            for (let i = shuffled.length - 1; i > 0; i--) {
              
                const j = Math.floor(Math.random() * (i + 1));
        
              
                [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
            }
        
            return shuffled;
        }
        function alan_ekle(alanlar) {
            var bilgi_formu = document.querySelector('.bilgi-formu');
            var htmlContent = '';
            
            for (let i = 0; i < alanlar.length; i++) {
                let inputType = alanlar[i].fields.type;
                let additionalAttributes = "";
                let additionalAttributes1 = "";
                let additionalAttributes2 = "";
                let optionsArray = alanlar[i].fields.options.split(';');
                let optionsHTML = optionsArray.map(option => `<option value="${option}">${option}</option>`).join('');
        
                if (alanlar[i].fields.slug === "quiz_attr_5") {
                    inputType = "text";
                    additionalAttributes1 = "05xxxxxxx Formatı Zorunludur !";
                } else if (alanlar[i].fields.slug === "quiz_attr_6") {
                    inputType = "email";
                    additionalAttributes = 'required';
                    additionalAttributes1 = "info@mail.com Formatı Zorunludur !";
                }
        
                htmlContent += (inputType === "text" || inputType === "tel" || inputType === "email") 
                    ? `<div class="form-group">
                           <label for="${alanlar[i].fields.slug}" class="mb-1 mt-3">${alanlar[i].fields.name}</label>
                           <input type="${inputType}" name="${alanlar[i].fields.slug}" class="form-control bilgi-formu-a" placeholder="${additionalAttributes1}" ${additionalAttributes}>
                       </div>`
                    : `<div class="form-group">
                           <label for="${alanlar[i].fields.slug}" class="mb-1 mt-3">${alanlar[i].fields.name}</label>
                           <select name="${alanlar[i].fields.slug}" class="form-control bilgi-formu-a" required>   
                               <option value="">Seçiniz</option>
                               ${optionsHTML}
                           </select>
                       </div>`;
        
            }
        
            htmlContent += `<div class="form-group">
                                <button type="button" class="btn btn-primary form-devam-et mt-3" style="background-color:rgb(9, 0, 57);" id="startButton" disabled> Devam Et </button>
                            </div>`;
            
            bilgi_formu.style.display = 'block';
            bilgi_formu.innerHTML = htmlContent;
        
            var telInput = document.querySelector('input[name="quiz_attr_5"]');
            var emailInput = document.querySelector('input[name="quiz_attr_6"]');
            var startButton = document.getElementById("startButton");
        
            function validateInputs() {
                let telValid = true;
            let emailValid = true;
        
            if (telInput) {
                telValid = telInput.value.match(/^\d{10}$/) || telInput.value.match(/^0\d{10}$/) || telInput.value.match(/^\+\d{2}\d{10}$/);
            }
        
            if (emailInput) {
                emailValid = emailInput.value.match(/^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,4}$/);
            }
                
                startButton.disabled = !(telValid && emailValid);
            }
        
            if (telInput) {
                telInput.addEventListener("input", function() {
                    this.style.border = (this.value.match(/^\d{10}$/) || this.value.match(/^0\d{10}$/) || this.value.match(/^\+\d{2}\d{10}$/))
                        ? "" : "2px solid red";
                    validateInputs();
                });
            }
        
            if (emailInput) {
                emailInput.addEventListener("input", function() {
                    this.style.border = this.value.match(/^[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,4}$/) ? "" : "2px solid red";
                    validateInputs();
                });
            }
        }
        
        
        function bilgi_formu_kontrol(){
            var formElements = document.querySelectorAll('.bilgi-formu-a');
          
            console.log("fonksiyon çalıştı;");
            var allFilled = true;
        
        for(let i = 0; i < formElements.length; i++) {
            if ((formElements[i].type === 'checkbox' || formElements[i].type === 'radio') && !formElements[i].checked) {
                allFilled = false;
                break;
            } 
            else if (formElements[i].value.trim() === "") {
                allFilled = false;
                break;
            }
        }
        if(allFilled){
            return true;
        } else {
            return false;
        }
        }
        function alanlar_kontrol(test_id) {
            var csrfToken = getCookie('csrftoken');
            var inputs = $('.bilgi-formu input, .bilgi-formu select').serialize();
            var formData = inputs + "&csrfmiddlewaretoken=" + csrfToken;
            $('.bilgi-formu input, .bilgi-formu select').each(function() {
                console.log('Element name:', $(this).attr('name'), 'Value:', $(this).val());
            });
            var k_adi = 0;
            console.log(formData)
        
            console.log("vsrf tokenb : ",csrfToken);
            return new Promise((resolve, reject) => {
                $.ajax({
                    url: "/panel/sonuc-oncesi/" + test_id,
                    type: 'POST',
                    data: formData,
                    dataType: 'json',
                    headers: {
                        'X-CSRFToken': csrfToken
                    },
                    success: function(response) {
                        if (!response.id) {
                            resolve(false);
                        } else {
                            resolve(response.id);
                        }
                    },
                    error: function() {
                        console.error("AJAX isteği başarısız.");
                        reject(new Error("AJAX isteği başarısız."));
                    }
                });
            });
        }
        
        function getCookie(name) {
            var value = "; " + document.cookie;
            var parts = value.split("; " + name + "=");
            if (parts.length == 2) return parts.pop().split(";").shift();
        }
        
        function submit_quiz() {
            var csrfToken = getCookie('csrftoken');
            var form = $('#quiz-form');
            if (form.length === 0) {
                console.error("quiz-form ID'li form bulunamadı.");
                return;
            }
            var formData = form.serialize();
        
            console.log(formData);
            
            console.log("token : ",csrfToken)
            $.ajax({
                url: "/panel/sonuclar/",
                type: 'POST',
                data: formData,
                dataType: 'json',
                headers: {
                        'X-CSRFToken': csrfToken
                    },
                success: function(response) {
                    console.log('Başarılıtest gösderildi ');
                    console.log('Başarılı:', response);
                },
                error: function(error) {
                    console.log('Başarılıtest gösderildiaaa ');
                    console.error('Hata:', error);
                }
            });
        }
        
        $(document).ready(function()
        {
            
            $('.sertifika').on('click', function() { 
                sertifikaS();
            });
        
            $(".step-bar .bar .fill").eq(now).addClass('w-100');
            
            window.onbeforeunload = function() {
            return "Sayfayı yenilemek istediğinize emin misiniz?";
            };
        
            var inputElement = document.getElementById("quiz_id");
            
            var deger = inputElement.value;
            $.ajax({
                url: "/panel/quiz_ajax/"+deger ,
                method: "GET",
                dataType: "json", 
                success: function(response) {
                    var option = response.options;
                    var soru_adedi = response.soru_adedi;
                    var sorular = JSON.parse(response.sorular);
                    var cevaplar = JSON.parse(response.cevaplar);
                    var interval = response.intervals;
                    var kullanici_formu = response.kullanici_formu;     
                    var time = option.timer;
                    var make_questions_required = option.make_questions_required;  
                    var randomize_questions = option.randomize_questions;
                    var randomize_answers = option.randomize_answers;
                    var enable_autostart = option.enable_autostart;
                    var timer_text = option.timer_text;
                    var yanlis_soru = response.yanlis_soru;
                    var alanlar_ = response.alanlar;
                    var alanlar = JSON.parse(alanlar_);
                    var sertifika = option.enable_certificate;
                    var published = response.published;
                    console.log("bbbb : " , published)
                    $('.questions-card').hide();
                    const quizInput = document.getElementById('quiz_id');
                    var timer_div = document.getElementById('timerDiv');
                    if (quizInput.value === getCookie('lastQuizTaken')) {
                    document.getElementById("overlay2").style.display = "block"; 
                    
                    document.body.style.overflow = "hidden"; 
                    timer_div.style.display = 'none';
                    }
        
                    if(published == 0){
                    document.getElementById("overlay").style.display = "block"; 
                    document.body.style.overflow = "hidden"; 
                    timer_div.style.display = 'none';
                    }
        
                    var sertifika_ = document.querySelector(".ser_kont");
                    if(sertifika=="off"){
                        console.log("sertifika kapalı")
                        sertifika_.remove();
                    }
                    if(randomize_questions == "on"){
                        sorular = shuffleArray(sorular);
                    }
                    if(randomize_answers == "on"){
                        cevaplar = shuffleArray(cevaplar);
                    }
                    console.log("yanlis_soru:",yanlis_soru)
                    if (yanlis_soru === "on") {
                        document.addEventListener('change', function(e) {
                            if (e.target && e.target.type === 'radio') {
                                handleRadioChange(e.target);
                            }
                        });
                    }
                    
                    if(kullanici_formu == 0 && enable_autostart == "off"){
                        var timer_text1 = option.timer_text;
                        var centered_card = document.getElementById('centered-card');
                        var centered_content = document.getElementById('card-content-c');
                        var custom_container = document.getElementById('custom-container');
                        centered_content.innerHTML = timer_text1;
                        centered_card.style.display = 'block';
                        document.getElementById('modal-background').style.display = 'block';
                        custom_container.style.display = 'none';
                        enable_autostart == "on"
                        var baslatButton = document.getElementById("baslat");
                        
                        baslatButton.addEventListener("click", function() {
                            centered_card.style.display = 'none';
                            document.getElementById('modal-background').style.display = 'none';
                            timer_div.style.display = 'block';
                            setCookie("visitedBefore", "true", 1);
                            zaman_takip(time); 
                            kayit_formu.style.display = 'none';
                            onAjaxSuccess(response.soru_adedi,sorular,cevaplar);
                            transferContent();
                            step1kaldir();
                            overOP();
                            enable_navigation_bar();
                        });
                    }
                    
                    
                    timer_div.style.display = 'none';
                    var kayit_formu = document.querySelector('.custom-container');
                    kayit_formu.style.display = 'none';
                   
                    let getcookie = getCookie("visitedBefore");
                    if(kullanici_formu == 1){
                        if( !getcookie ){
                            kayit_formu.style.display = 'block';
                            alan_ekle(alanlar);
                            console.log(alanlar.length)
                           
                        }else{
                            timer_div.style.display = 'block';
                            console.log("if'egirdi:")
                            getcookie = getCookie("visitedBefore");
                            setCookie("visitedBefore", "true", 1); 
                            console.log("coocie: ",getcookie);
                            onAjaxSuccess(response.soru_adedi,sorular,cevaplar);
                            transferContent();
                            zaman_takip(time); 
                            step1kaldir();
                            overOP();
                            enable_navigation_bar();
                        }
                    }else if(kullanici_formu == 0 && enable_autostart == "on"){
                        const timer_divs = document.getElementById('timerDiv');
                        timer_divs.style.display = 'block';
                        onAjaxSuccess(response.soru_adedi,sorular,cevaplar);
                        zaman_takip(time); 
                        transferContent();
                        step1kaldir();
                        overOP();
                        enable_navigation_bar();
                        console.log("else'e girdi:")
                    }
                   
                   var btn = document.querySelector('.form-devam-et');
                   if(btn){
                    btn.addEventListener('click', function() {
                        
                        var quizIDValuae = $('#quiz_id').val();
                        var timer_text1 = option.timer_text;
                        console.log("id : ",quizIDValuae)
                        alanlar_kontrol(quizIDValuae).then(result => {
                            console.log(result);
                            const quizInput = document.getElementById('quiz_id');
                            console.log(quizInput.value,getCookie('lastQuizTaken'))
                           
                            if (!result) {
                            if (quizInput.value === getCookie('lastQuizTaken2')) {
                                $('#warning-card').show();
                                timer_div.style.display = 'none';
        
                                $('body').append('<div class="background-overlay"></div>');
                            
                            
                                $('body').addClass('blurred');
                            }else{
                                document.cookie = "lastQuizTaken2=" + quizInput.value;
                                var k_id = document.getElementById('k_id');
                                k_id.value=result;
                            }
                            }else
                            {
                                var k_id = document.getElementById('k_id');
                                k_id.value=result;
                            }
                        }).catch(error => {
                            console.error(error);
                        });
                        
                        var adSoyadInput = document.getElementById('ad-soyad');
                        var okulInput = document.getElementById('okul');
                        var sinifInput = document.getElementById('sinif');
                        var centered_card = document.getElementById('centered-card');
                        var centered_content = document.getElementById('card-content-c');
                        var custom_container = document.getElementById('custom-container');
                        const timer_div = document.getElementById('timerDiv');
                        var bilgi_formu_kontrol_ = bilgi_formu_kontrol();
                        console.log(bilgi_formu_kontrol_)
                        if (bilgi_formu_kontrol_ == true) {
                            if(enable_autostart == "off"){
                                centered_content.innerHTML = timer_text1;
                                centered_card.style.display = 'block';
                                custom_container.style.display = 'none';
                                enable_autostart == "on"
                                var baslatButton = document.getElementById("baslat");
                                baslatButton.addEventListener("click", function() {
                                    centered_card.style.display = 'none';
                                timer_div.style.display = 'block';
                                setCookie("visitedBefore", "true", 1);
                                zaman_takip(time); 
                                kayit_formu.style.display = 'none';
                                onAjaxSuccess(response.soru_adedi,sorular,cevaplar);
                                transferContent();
                                step1kaldir();
                                overOP();
                                enable_navigation_bar();
                                });
                            }else{
                            timer_div.style.display = 'block';
                            setCookie("visitedBefore", "true", 1);
                            zaman_takip(time); 
                            kayit_formu.style.display = 'none';
                            onAjaxSuccess(response.soru_adedi,sorular,cevaplar);
                            transferContent();
                            step1kaldir();
                            overOP();
                            enable_navigation_bar();
                        }
                        } else {
                            alert("Lütfen tüm alanları doldurunuz.");
                        }
                    });}
        
                    
                 
                    function step1kaldir(){
                    const step1Form = document.getElementById('step1');
                    const prevButton = step1Form.querySelector('.prev');
                    console.log("devam etti");
                    if (prevButton) {
                        prevButton.remove();
                    }
                    }
        
                    function enable_navigation_bar(){
                    if(option.enable_navigation_bar == "off"){
                        let prevbuttons = document.querySelectorAll('.prev');
                        prevbuttons.forEach(button => {
                        button.style.display = "none";
                    });
                    }
                    }
                        
                    function overOP(){
                        const stepForm = document.getElementById('step' + soru_adedi);
            
            var radio_divs = document.querySelectorAll('.radio-field');
            
            radio_divs.forEach(div => {
                var img = div.querySelector('img');
                var input = div.querySelector('input');
                if (img) {
                    var srcValue = img.getAttribute('src'); 
                    if (srcValue && srcValue.trim() !== "") {  
                        div.classList.add('img-op');
                        div.classList.add('image-radio-wrapper');
                        var parentDiv = div.parentElement;
                        parentDiv.classList.add('answer-container2');
                    } else if (srcValue === "null" || srcValue.trim() === "") {
                        img.style.display = "none";
                    }
                }
            });
        
        
        
                    const headings = document.querySelectorAll('.q-heading');
                    headings.forEach(function(heading) {
                        heading.innerHTML = transformContent(heading.innerHTML);
                        });
                       
                    
                        
                    
                    $(".step-btn").on('click', function()
                         {
                            var now=0;
                            var dataId = $(this).data('id');
                            console.log("next çaloıştı",dataId);
                             radiovalidate(dataId); 
                             if(checkedradio == false && make_questions_required == "on" )
                             {
                             (function (el) {
                                 setTimeout(function () {
                                     el.children().remove('.reveal');
                                 }, 3000);
                                 }($('#error').append('<div class="reveal alert alert-danger">Lütfen bir cevabı seçin !</div>')));
        
                                 radiovalidate(dataId);
                             
                             }
        
                             else
                             {
                                 $('[data-id="' + dataId + '"]').find('.radio-field').removeClass('bounce-left');
                                 $('[data-id="' + dataId + '"]').find('.radio-field').addClass('bounce-right');
                                 setTimeout(function()
                                 {
                                     now = next(soru_adedi,'.section-container section');
        
                                 }, 900)
                             
                                 countresult(dataId);
                                 
                             
                             }
                                 
                             
                             
                             
                         
                         })
                         var divs = $('.section-container section');
                         $(".prev").on('click', function()
                    {
        
                        console.log("prev çalıştı");
                        $('.radio-field').addClass('bounce-left');
                        $('.radio-field').removeClass('bounce-right');
                        $(".step-bar .bar .fill").eq(now).removeClass('w-100');
                        divs.eq(now).hide();
                        now = (now > 0) ? now - 1 : divs.length - 1;
                        divs.eq(now).show(); // show previous
                        console.log(now);
                        transferContent();
                        showActiveStep();
                    
                    })
                    
                    $("#sub").on('click', function()
                    {event.preventDefault()
                        puan_hesapla(soru_adedi,interval,option);
                        radiovalidate(soru_adedi);
                        submit_quiz();
                        console.log("submitten sonrası")
                        if(checkedradio == false)
                        {
        
                        (function (el) {
                            setTimeout(function () {
                                el.children().remove('.reveal');
                            }, 3000);
                            }($('#error').append('<div class="reveal alert alert-danger">Choose an option!</div>')));
                            radiovalidate(soru_adedi);
                        }
                        else
                        {
                            countresult(soru_adedi);
                            showresult();
                        }
                    })
                }
        
        
            
        
                    stepbarcreate(response.soru_adedi);
                    showActiveStep(response.soru_adedi);
                    console.log(response.soru_adedi);
                    console.error("Geçerli bir 'count' değeri alınamadı.");
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log("hata");
                }
            });
        
        
            
            
          
        })