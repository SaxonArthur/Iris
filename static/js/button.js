//Allows for js to interact with these elements
const mic=document.getElementById('mic-btn');
const submit=document.querySelector('.hidden');
const playback=document.querySelector('.playback');
const refreshbtn=document.getElementById('refresh');

//Animations for mic button
mic.addEventListener('mouseenter', () => {
    mic.classList.add('mic-btn-hover-on');
    mic.classList.remove('mic-btn-hover-off')
})
mic.addEventListener('mouseleave', () => {
    mic.classList.remove('mic-btn-hover-on');
    mic.classList.add('mic-btn-hover-off');
})


mic.addEventListener('click', ToggleMic);

refreshbtn.addEventListener('click', Refreshlog)
    
//Function to Refresh the message log
async function Refreshlog (){
     const refreshresponse = await fetch('http://127.0.0.1:5000/refresh', { //Sends signal to backend
        method:'post',
    });
    const transcription = await refreshresponse.json();
    console.log(transcription.text);
};

let can_record = false;
let is_recording = false;

let recorder = null;

let chunks = [];


//Checks permissions
function SetupAudio(){
    console.log('Setup')
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia){
        navigator.mediaDevices
            .getUserMedia({
                audio:true
            })
            .then(SetupStream)
            .catch(err =>{console.error(err)});
    }
}

SetupAudio();

//Records audio
function SetupStream(stream){
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => {
        chunks.push(e.data);
    }
    recorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm; codecs=opus' }); //Packages audio
        chunks=[]
        const formData = new FormData();
        formData.append('audio', audioBlob, 'recording.webm');
        const response = await fetch('http://127.0.0.1:5000/upload', { //Sends to backend
            method: 'post',
            body: formData,
        });

        const transcription = await response.json();
        console.log(transcription.text); // Handle the transcription
        window.location.replace("http://127.0.0.1:5000/response"); //Redirects browser to response page

    };
    can_record=true;

}
//Function that checks if Mic is recording when clicked
function ToggleMic(){
    if (!can_record) return;
    
    is_recording=!is_recording;

    if (is_recording){
        recorder.start();
        mic.classList.add('pulse');
    } else{
        recorder.stop();
        mic.classList.remove('pulse');
    }
}