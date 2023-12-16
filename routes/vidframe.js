const path = require('path');

const express = require('express');

const availableUser = require('./../Database/mongoose').availableUser;
// const adminController = require('../controllers/admin');

const router = express.Router();                         //basically , using this to route our stuff throu files.

sumPg = (req , res , next ) =>{
    res.render('sumpg');
}

router.get('/sum' , sumPg); 


router.post('/login' , (req, res, next) =>{
  // res.sendFile(path.join(__dirname, 'public', 'contact.html'));
  // res.render('contact');
  const email_value = req.body.email ;
  const pswd_value = req.body.password ;
  // console.log(email_value);
  if (availableUser(email_value , pswd_value)){
    console.log("correct user");
    res.render('index');
  };
  


})

router.get('/login' , (req, res, next) =>{
  res.render('contact');
});


let currentFrame = ''; 

router.get('/receive_frame', (req, res) => {
  console.log("running on rcv frame get");
    const { frame } = req.body;

    currentFrame = frame; 
    // res.redirect('/display_frames');
    console.log('Frame ');

    res.send(currentFrame);

  }
);


router.post('/receive_frame', (req, res) => {
    const { frame } = req.body;

    currentFrame = frame; // Update the current frame

    // console.log('Frame ');

    res.status(200).send("Frame received");

    }
);

router.post('/send-frame' , (req , res , next) =>{
  // console.log("the data being sent to the ejs is :" , currentFrame);
  res.send(currentFrame);
})





router.get('/display_frames1', (req, res) => {

    res.render('mainpg.ejs', {
      myFrame : currentFrame ,
    });
    
    // setTimeout(() => {
    //   res.redirect('/receive_frame');
    // }, 3000);

  });


router.get('/display_frames2', (req, res) => {

    res.render('mainpg2.ejs', {
      myFrame : currentFrame ,
    });
    
    // setTimeout(() => {
    //   res.redirect('/receive_frame');
    // }, 3000);

  });

router.get('/display_frames3', (req, res) => {

    res.render('mainpg3.ejs', {
      myFrame : currentFrame ,
    });
    
    // setTimeout(() => {
    //   res.redirect('/receive_frame');
    // }, 3000);

  });




  

// router.post('/display_frames', (req, res) => {
//   console.log("running");
// });

router.post('/delete_frame', (req, res) => {
  console.log("running");
    
  
    res.redirect('/receive_frame');
  });


module.exports = router;