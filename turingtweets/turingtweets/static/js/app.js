'use strict';

var fake;
var real;

function setFakeTweet() {
    $('#left-tweet').hide();
    $('#right-tweet').hide();
    var realTweet = $('#left-tweet').text();
    real = realTweet;
    var fakeTweet = $('#right-tweet').text();
    fake = fakeTweet;
    var randPos = Math.floor(Math.random() * 2) + 1;

    if (randPos === 2) {
        $('#right-tweet').text(realTweet);
        $('#left-tweet').text(fakeTweet);
        $('#left-tweet').show();
        $('#right-tweet').show();
    }
    else {
        $('#left-tweet').show();
        $('#right-tweet').show();
    }
}

$('#left-tweet').click(function() {
    if ($('#left-tweet').text() == real) {
        $('.white-text').text('Correct!');
    }
    else {
        $('.white-text').text('Incorrect! SAD');
    }
    $('.button').show();
});

$('#right-tweet').click(function() {
    if ($('#right-tweet').text() == real) {
        $('.white-text').text('Correct!');
    }
    else {
        $('.white-text').text('Incorrect! SAD');
    }
    $('.button').show();
});

$('.button').click(function() {
    location.href = '/';
});