//If only using a single js file without imports msj extension can be changed to js


import { InitiativeTracker } from "./initiativeTracker.mjs";

window.onload = main

function main(){
    initializeButtons();
    
    iT.add("Oni", 3, 5);
    iT.add("Galifraen", 3);
    iT.add("Zodious",1);
    iT.add("Moa",1);
    iT.add("Everin",1);
    iT.add("Stool",1);
    iT.add("Seven Stars",1);   
    iT.sort()
}

function initializeButtons(){
    $("button#addBtn").click(function(){
        iT.add($("#nameInput")[0].value, $("#initInput")[0].value)
    })
    $("#sortItemsBtn").click(function(){
        iT.sort();
    })
    $("#cycleBtn").click(function(){
        iT.cycle();
    })
    $("#rerollAllBtn").click(function(){
        iT.rerollAll();
    })
}

let iT = new InitiativeTracker();



