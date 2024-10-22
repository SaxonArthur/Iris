 const geolocate = async () => {
    const json = await fetch('https://ipapi.co/json/'); //Gets location of user
    const info = await json.json();
    const formData = new FormData(); 
    formData.append('location', +info['latitude']+','+info['longitude']+','+info['city']);  //Formats useful data
    const response = await fetch('http://127.0.0.1:5000/locate', { 
            method: 'post',
            body: formData
    });
    const transcription = await response.json();
    console.log(transcription.text); // Handle the transcription
};

geolocate();