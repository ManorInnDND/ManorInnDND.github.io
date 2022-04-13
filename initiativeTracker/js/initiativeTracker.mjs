export {InitiativeTracker}

class InitiativeTracker{
    constructor(){
        this.table = document.getElementById("initTable");
        this.nextItemID = 0;
        this.table.innerHTML = "<tr><th>Name</th><th>Roll</th><th>Bonus</th><th>Reroll?</th></tr>"
    }

    _reroll(event){
        let target = event.target;
        var initBonus;
        if(!isNaN(parseInt( target.initBonusCell.textContent))){
             initBonus = parseInt(target.initBonusCell.textContent);
        } else{
            initBonus = 0;
            target.initBonusCell.textContent = initBonus
        };

        let dieRoll = Math.ceil(Math.random()*20);
        target.initCell.textContent = dieRoll + initBonus;    
    }

    add(name, initValue, initBonus){
        let row = document.createElement("tr");
        row.setAttribute("name", this.nextItemID)
        
        let nameCell = document.createElement("td");
        nameCell.setAttribute("contenteditable", "true");
        nameCell.setAttribute("name", "nameCell")
        nameCell.textContent = name

        let initCell = document.createElement("td");
        initCell.setAttribute("name", "initCell");
        initCell.setAttribute("contenteditable", "true");
        initCell.textContent = initValue;

        let initBonusCell = document.createElement("td");
        if(initBonus){
            initBonusCell.textContent = initBonus
        } else {initBonusCell.textContent = 0}

        let rerollCell = document.createElement("td");
        let rerollButton = document.createElement("button");
        rerollButton.setAttribute("name", "rerollBtn");
        rerollButton.initBonusCell = initBonusCell;
        rerollButton.initCell = initCell;
        rerollButton.onclick = this._reroll;
        rerollCell.appendChild(rerollButton)

        row.append(nameCell, initCell, initBonusCell, rerollCell);
        this.table.appendChild(row);

        this.nextItemID++;
    }

    sort(){
        var rows, switching, i, x, y, shouldSwitch;
        switching = true;

        while (switching){
            switching = false;
            rows = this.table.rows
            for (i=1; i<(rows.length - 1);i++) {
                shouldSwitch = false;
                x = parseInt(rows[i].querySelector("td[name=initCell]").textContent);
                y = parseInt(rows[i + 1].querySelector("td[name=initCell]").textContent);
                if(x < y){
                    shouldSwitch = true;
                    break;
                }
            }
            if (shouldSwitch){
                rows[i].parentNode.insertBefore(rows[i+1], rows[i]);
                switching = true;
            }
        }
    }

    cycle(){
        var rows = this.table.rows
        var currentRow = this.table.querySelector("tr.current");
        var currentIndex, nextIndex;
        if(currentRow){
            currentIndex = currentRow.rowIndex;
        } else {
            currentIndex = 0;
        }
        if(currentIndex == rows.length - 1){
            nextIndex = 1;               
        } else {
            nextIndex = currentIndex + 1
        }
        rows[nextIndex].setAttribute("class", "current");
        rows[nextIndex].scrollIntoView()
        rows[currentIndex].removeAttribute("class");
    }

    rerollAll(){
        let buttons = this.table.querySelectorAll("button[name=rerollBtn]");
        for(var button of buttons){
            button.click()
        }
    }




}
