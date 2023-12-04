const bodyParser = require('body-parser');
const path = require('path');


const express = require('express');            
const app = express();    

app.set('view engine' , 'ejs');            
app.set('views' , 'views');   

app.use(express.urlencoded({ limit: '50mb', extended: false }));          
app.use(express.json({ limit: '50mb' })); 
app.use(express.static(path.join(__dirname , 'views')));

const vidRoute = require('./routes/vidframe');
app.use(vidRoute);



app.listen(4000);  