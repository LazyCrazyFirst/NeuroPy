let microfonBlockElement = document.querySelector(".microfon__block");
let tog = 1;
let show = document.querySelector(".show");
let krest = document.querySelector(".krest")

microfonBlockElement.addEventListener("click",()=>{
  
    microfonBlockElement.style.opacity="0";
    show.style.marginBottom = "0";
  
 
});

krest.addEventListener("click",()=>{
 
    microfonBlockElement.style.opacity="1";
    show.style.marginBottom = "-200px";
   
  
});
