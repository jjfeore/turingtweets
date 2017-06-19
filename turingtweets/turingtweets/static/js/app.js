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

$('.div-tweet-photo-text').eq(0).click(function() {
    if ($('#left-tweet').text() == real) {
        $('.h2-white-text').text('Correct!');
        $('.h2-white-text').css('text-shadow', '0px 0px 15px #00FF00');
        $('.h2-white-text').css('color', 'rgba(0, 0, 0, 0.6)');
        $('.div-tweet-photo-text').eq(0).css('box-shadow', '0px 0px 15px #00FF00');
        $('.div-tweet-photo-text').eq(1).css('box-shadow', '0px 0px 15px #FF0000');
        $('.button').css('background-color', 'rgba(0, 255, 0, 0.6)');
        $('.button').css('color', 'rgba(0, 0, 0, 0.6)');
    }
    else {
        $('.h2-white-text').text('Incorrect!');
        $('.h2-white-text').css('text-shadow', '0px 0px 15px #FF0000');
        $('.h2-white-text').css('color', 'white');
        $('.div-tweet-photo-text').eq(1).css('box-shadow', '0px 0px 15px #00FF00');
        $('.div-tweet-photo-text').eq(0).css('box-shadow', '0px 0px 15px #FF0000');
        $('.button').css('background-color', 'rgba(255, 0, 0, 0.6)');
        $('.button').css('color', 'white');
        $('#twitter-info').show();
        $.post('/', {fakeTweet:fake});
    }
    $('.button').show();
    $('.div-tweet-photo-text').off('click');
});

$('.div-tweet-photo-text').eq(1).click(function() {
    if ($('#right-tweet').text() == real) {
        $('.h2-white-text').text('Correct!');
        $('.h2-white-text').css('text-shadow', '0px 0px 15px #00FF00');
        $('.h2-white-text').css('color', 'rgba(0, 0, 0, 0.6)');
        $('.div-tweet-photo-text').eq(1).css('box-shadow', '0px 0px 15px #00FF00');
        $('.div-tweet-photo-text').eq(0).css('box-shadow', '0px 0px 15px #FF0000');
        $('.button').css('background-color', 'rgba(0, 255, 0, 0.6)');
        $('.button').css('color', 'rgba(0, 0, 0, 0.6)');
    }
    else {
        $('.h2-white-text').text('Incorrect!');
        $('.h2-white-text').css('text-shadow', '0px 0px 15px #FF0000');
        $('.h2-white-text').css('color', 'white');
        $('.div-tweet-photo-text').eq(0).css('box-shadow', '0px 0px 15px #00FF00');
        $('.div-tweet-photo-text').eq(1).css('box-shadow', '0px 0px 15px #FF0000');
        $('.button').css('background-color', 'rgba(255, 0, 0, 0.6)');
        $('.button').css('color', 'white');
        $('#twitter-info').show();
        $.post('/', {fakeTweet:fake});
    }
    $('.button').show();
    $('.div-tweet-photo-text').off('click');
});

$('.button').click(function() {
    location.href = '/';
});