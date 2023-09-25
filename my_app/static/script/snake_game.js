const canvas = document.getElementById("game");
const ctx = canvas.getContext('2d');

class SnakePart
{
    constructor(x,y)
    {
        this.x = x;
        this.y = y;
    }
}

let gameId =1;
let score = 0;
let scoreObj = {};
let getScoreObj = {};
let userBest = 0;
let gameBest = 0;
let userPrev = 0;
let speed = 3;
let xVelocity = 0;
let yVelocity = 0;

let tileCount = 20;
let tileSize = canvas.width/tileCount -2;

let headX = 10;
let headY = 10;
const snakeParts = [];
tailLength = 0;


let appleX = Math.floor(Math.random()*tileCount);
let appleY = Math.floor(Math.random()*tileCount);

function menu()
{
    window.reload();
}


function drawGame()
{
 //   let result = (score%8);
//    console.log(result);
//    console.log("speed: "+speed+" => "+(score%8));

    getGameStats();
    changeSnakePos();
    if (isGameOver())
    {
        sendScore();
        // getGameStats();
        // bestScore();
        return gameOver();
    }
    clearScreen();

    checkAppleCollision();
    drawApple();
    drawSnake();
//    drawScore();
    setTimeout(drawGame, 1000/speed);

    // console.log(isGameOver());
    // console.log("headx: "+headX);
    // console.log("heady: "+headY);
    // console.log(canvas.width);
    // console.log(canvas.height);
}

function drawScore()
{
    ctx.fillStyle = 'white';
    ctx.font = "20px Verdana";
    ctx.fillText("Score: " + score, canvas.width-100, 20);
}


function clearScreen()
{
    ctx.fillStyle = 'black';
    ctx.fillRect(0,0, canvas.width, canvas.height);
}

function drawSnake()
{
    ctx.fillStyle = 'green';
    for (let i = 0; i < snakeParts.length; i++)
    {
        let part = snakeParts[i];
        ctx.fillRect(part.x*tileCount, part.y*tileCount, tileSize, tileSize);
    }

    snakeParts.push(new SnakePart(headX, headY));
    if (snakeParts.length > tailLength)
    {
        snakeParts.shift();
    }

    ctx.fillStyle = 'blue';
    ctx.fillRect(headX*tileCount, headY*tileCount, tileSize, tileSize);

}

function drawApple()
{
    ctx.fillStyle = 'red';
    ctx.fillRect(appleX*tileCount, appleY*tileCount, tileSize, tileSize);
}

function checkAppleCollision()
{
    if ((appleX == headX) && (appleY == headY))
    {
        newApplePos();
        tailLength++;
        score++;
        if (score%8 === 0) speed++;
    }
}

function newApplePos()
{
    x = Math.floor(Math.random()*tileCount);
    y = Math.floor(Math.random()*tileCount);
    for (let i = 0; i < tailLength; i++)
    {
        let part = snakeParts[i];
        if ((part.x === x) && (part.y === y)) return newApplePos();
    }
    appleX = x;
    appleY = y;
    return
}

function isGameOver()
{
    let over = false;

    if ((xVelocity === 0) && (yVelocity === 0)) return false;

    // if (headX < 0) over = true;
    // else if (headX >= tileCount)  over = true;
    // else if (headY < 0) over = true;
    // else if (headY >= tileCount) over = true;
    if (headX < 0) return true;
    else if (headX >= tileCount)  return true;
    else if (headY < 0) return true;
    else if (headY >= tileCount) return true;

    for (let i = 1; i < snakeParts.length; i++)
    {
        // console.log("partx: "+part.x)
        // console.log("party: "+part.y)
        let part = snakeParts[i];
        if ((headX === part.x) && (headY === part.y))
        {
            return true;
        }
    }
}

function gameOver()
{
    ctx.fillStyle = "white";
    ctx.font = "50px Verdana";

    let gradient = ctx.createLinearGradient(0,0,canvas.width, 0);
    gradient.addColorStop("0", "magenta");
    gradient.addColorStop("0.5", "blue");
    gradient.addColorStop("1.0", "red");
    ctx.fillStyle = gradient;
    ctx.fillText("GAME OVER", canvas.width/6.5, canvas.height/2);
}


function changeSnakePos()
{
    headX = headX + xVelocity;
    headY = headY + yVelocity;
}


document.body.addEventListener('keydown', keyDown);

function keyDown(event)
{
    //up
    if (event.keyCode == 38)
    {
        if (yVelocity == 1) return;
        yVelocity = -1;
        xVelocity = 0;
    }
    //down
    if (event.keyCode == 40)
    {
        if (yVelocity == -1) return;
        yVelocity = 1;
        xVelocity = 0;
    }
    //left
    if (event.keyCode == 37)
    {
        if (xVelocity == 1) return;
        yVelocity = 0;
        xVelocity = -1;
    }
    //right
    if (event.keyCode == 39)
    {
        if (xVelocity == -1) return;
        yVelocity = 0;
        xVelocity = 1;
    }

}

// function bestScore()
// {
//     if (score>best) best = score;
//     return best;
// }

function postMyScore()
{
    document.getElementById("score").innerText= "Score: "+score;
    //let element = document.getElementById("score").innerHTML = "Score: "+score;
    //element.innerText = "Score: "+score;
}

function displayStats()
{
    // getGameStats();

    console.log(userBest, userPrev, gameBest, score)

    document.getElementById("myprev").innerText= "Previous Score: "+prev;
    document.getElementById("userbest").innerText= "Personal Best: "+userBest;
    document.getElementById("gamebest").innerText= "Personal Best: "+gameBest;
    document.getElementById("score").innerText = "Score: "+score;
    // getGameStats();
    // userbest = getScoreObj.['user_best'];
    // prev = getScoreObj['user_prev'];
    // gameBest = getScoreObj['game_best'];
    // document.getElementById("#myprev").innerText= "Previous Score: "+prev;
    // document.getElementById("#userbest").innerText= "Personal Best: "+userBest;
    // document.getElementById("#gamebest").innerText= "Personal Best: "+gameBest;
    // document.getElementById("#score").innerText = "Score: "+score;
    //element.innerText = "Score: "+score;
}

// how do get game_id from html
function sendScore()
{
    scoreObj =
    {
        "score": score,
        "game_id":gameId,
        "user_id":userId,
        "score_id":scoreId,
        "gameBest_id": gameBestId
    }
    $.ajax
    ({
        url: "/updateScore/"+gameId,
        contentType: "application/json",
        type: 'POST',
        dataType: "json",
        data: JSON.stringify(scoreObj),
        success: function(response)
        {
            console.log(response);
        },
        error: function(error)
        {
            console.log(error);
        }
    });
    // e.preventDefault();
}


function getGameStats()
{
    $.ajax
    ({
        url: "/updateScore/"+gameId,
        contentType: "application/json",
        type: 'GET',
        dataType: "json",
        // data: $.  stringify(scoreObj),
        // {'game_best': game_bests.best_score, 'user_best': user_scores.best_score, 'user_prev': user_scores.prev_score}
        success: function(response)
        {
            top_scores = response.top_scores
            userBest = response.user_best;
            userPrev = response.user_prev;
            gameBest = response.game_best;
            gameBestId = response.game_best_id;
            scoreId = response.score_id;
            userId = response.user_id;
            gameId = response.game_id;

            document.getElementById("myprev").innerText= "Previous Score: "+userPrev;
            document.getElementById("userbest").innerText= "Personal Best: "+userBest;
            document.getElementById("gamebest").innerText= "Game Best: "+gameBest;
            document.getElementById("score").innerText = "Current Score: "+score;
            console.log(userBest, userPrev, gameBest, score)

            // console.log(userBest, userPrev, gameBest)
            // console.log(response);
            // console.log("response: "+getScoreObj['user_best'])
        },
        error: function(error)
        {
            console.log(error);
        }
    });
    // e.preventDefault();
}



$('#sendScore').click(function(e) {
    scoreObj = {
        "score": score
    }
    $.ajax({
        url: "/updateScore",
        contentType: "application/json",
        type: 'POST',
        dataType: "json",
        data: JSON.stringify(scoreObj),
        success: function(response) {
            console.log(response);
        },
        error: function(error) {
            console.log(error);
        }
    });
    e.preventDefault();
});

// $("#mydiv").click(function() {alert("Hello there");});

// function sendScore()
// {
//     scoreObj = {
//         "score": score
//     }

//     console.log(scoreObj);

//     fetch('${window.origin}/updateScore'),
//         {
//         method: "POST",
//         credentials: "include",
//         body: JSON.stringify(scoreObj),
//         cache: "no-cache",
//         headers: new Headers({
//             "content-type": "application/json"})
//         }

// }
getGameStats();
drawGame();
