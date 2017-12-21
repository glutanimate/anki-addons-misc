# -*- coding: utf-8 -*-

"""
This file is part of the Let It Snow! add-on for Anki

Copyright: (c) 2017 Glutanimate <https://glutanimate.com/>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>

Uses snowfall.js by loktar00 (https://github.com/loktar00/JQuery-Snowfall),
    licensed under the Apache license 2.0
"""

from aqt.reviewer import Reviewer
from anki.hooks import wrap

from anki import version as anki_version
anki21 = anki_version.startswith("2.1.")

js_snow = r"""
if(!Date.now)
Date.now=function(){return new Date().getTime()};(function(){'use strict';var vendors=['webkit','moz'];for(var i=0;i<vendors.length&&!window.requestAnimationFrame;++i){var vp=vendors[i];window.requestAnimationFrame=window[vp+'RequestAnimationFrame'];window.cancelAnimationFrame=(window[vp+'CancelAnimationFrame']||window[vp+'CancelRequestAnimationFrame'])}
if(/iP(ad|hone|od).*OS 6/.test(window.navigator.userAgent)||!window.requestAnimationFrame||!window.cancelAnimationFrame){var lastTime=0;window.requestAnimationFrame=function(callback){var now=Date.now();var nextTime=Math.max(lastTime+16,now);return setTimeout(function(){callback(lastTime=nextTime)},nextTime-now)};window.cancelAnimationFrame=clearTimeout}}());(function($){$.snowfall=function(element,options){var flakes=[],defaults={flakeCount:35,flakeColor:'#ffffff',flakePosition:'absolute',flakeIndex:999999,minSize:1,maxSize:2,minSpeed:1,maxSpeed:5,round:!1,shadow:!1,collection:!1,collectionHeight:40,deviceorientation:!1},options=$.extend(defaults,options),random=function random(min,max){return Math.round(min+Math.random()*(max-min))};$(element).data("snowfall",this);function Flake(_x,_y,_size,_speed){this.x=_x;this.y=_y;this.size=_size;this.speed=_speed;this.step=0;this.stepSize=random(1,10)/100;if(options.collection){this.target=canvasCollection[random(0,canvasCollection.length-1)]}
var flakeMarkup=null;if(options.image){flakeMarkup=document.createElement("img");flakeMarkup.src=options.image}else{flakeMarkup=document.createElement("div");$(flakeMarkup).css({'background':options.flakeColor})}
$(flakeMarkup).attr({'class':'snowfall-flakes',}).css({'width':this.size,'height':this.size,'position':options.flakePosition,'top':this.y,'left':this.x,'fontSize':0,'zIndex':options.flakeIndex});if($(element).get(0).tagName===$(document).get(0).tagName){$('body').append($(flakeMarkup));element=$('body')}else{$(element).append($(flakeMarkup))}
this.element=flakeMarkup;this.update=function(){this.y+=this.speed;if(this.y>(elHeight)-(this.size+6)){this.reset()}
this.element.style.top=this.y+'px';this.element.style.left=this.x+'px';this.step+=this.stepSize;if(doRatio===!1){this.x+=Math.cos(this.step)}else{this.x+=(doRatio+Math.cos(this.step))}
if(options.collection){if(this.x>this.target.x&&this.x<this.target.width+this.target.x&&this.y>this.target.y&&this.y<this.target.height+this.target.y){var ctx=this.target.element.getContext("2d"),curX=this.x-this.target.x,curY=this.y-this.target.y,colData=this.target.colData;if(colData[parseInt(curX)][parseInt(curY+this.speed+this.size)]!==undefined||curY+this.speed+this.size>this.target.height){if(curY+this.speed+this.size>this.target.height){while(curY+this.speed+this.size>this.target.height&&this.speed>0){this.speed*=.5}
ctx.fillStyle=defaults.flakeColor;if(colData[parseInt(curX)][parseInt(curY+this.speed+this.size)]==undefined){colData[parseInt(curX)][parseInt(curY+this.speed+this.size)]=1;ctx.fillRect(curX,(curY)+this.speed+this.size,this.size,this.size)}else{colData[parseInt(curX)][parseInt(curY+this.speed)]=1;ctx.fillRect(curX,curY+this.speed,this.size,this.size)}
this.reset()}else{this.speed=1;this.stepSize=0;if(parseInt(curX)+1<this.target.width&&colData[parseInt(curX)+1][parseInt(curY)+1]==undefined){this.x++}else if(parseInt(curX)-1>0&&colData[parseInt(curX)-1][parseInt(curY)+1]==undefined){this.x--}else{ctx.fillStyle=defaults.flakeColor;ctx.fillRect(curX,curY,this.size,this.size);colData[parseInt(curX)][parseInt(curY)]=1;this.reset()}}}}}
if(this.x+this.size>(elWidth)-widthOffset||this.x<widthOffset){this.reset()}}
this.reset=function(){this.y=0;this.x=random(widthOffset,elWidth-widthOffset);this.stepSize=random(1,10)/100;this.size=random((options.minSize*100),(options.maxSize*100))/100;this.element.style.width=this.size+'px';this.element.style.height=this.size+'px';this.speed=random(options.minSpeed,options.maxSpeed)}}
var i=0,elHeight=$(element).height(),elWidth=$(element).width(),widthOffset=0,snowTimeout=0;if(options.collection!==!1){var testElem=document.createElement('canvas');if(!!(testElem.getContext&&testElem.getContext('2d'))){var canvasCollection=[],elements=$(options.collection),collectionHeight=options.collectionHeight;for(var i=0;i<elements.length;i++){var bounds=elements[i].getBoundingClientRect(),$canvas=$('<canvas/>',{'class':'snowfall-canvas'}),collisionData=[];if(bounds.top-collectionHeight>0){$('body').append($canvas);$canvas.css({'position':options.flakePosition,'left':bounds.left+'px','top':bounds.top-collectionHeight+'px'}).prop({width:bounds.width,height:collectionHeight});for(var w=0;w<bounds.width;w++){collisionData[w]=[]}
canvasCollection.push({element:$canvas.get(0),x:bounds.left,y:bounds.top-collectionHeight,width:bounds.width,height:collectionHeight,colData:collisionData})}}}else{options.collection=!1}}
if($(element).get(0).tagName===$(document).get(0).tagName){widthOffset=25}
$(window).bind("resize",function(){elHeight=$(element)[0].clientHeight;elWidth=$(element)[0].offsetWidth});for(i=0;i<options.flakeCount;i+=1){flakes.push(new Flake(random(widthOffset,elWidth-widthOffset),random(0,elHeight),random((options.minSize*100),(options.maxSize*100))/100,random(options.minSpeed,options.maxSpeed)))}
if(options.round){$('.snowfall-flakes').css({'-moz-border-radius':options.maxSize,'-webkit-border-radius':options.maxSize,'border-radius':options.maxSize})}
if(options.shadow){$('.snowfall-flakes').css({'-moz-box-shadow':'1px 1px 1px #555','-webkit-box-shadow':'1px 1px 1px #555','box-shadow':'1px 1px 1px #555'})}
var doRatio=!1;if(options.deviceorientation){$(window).bind('deviceorientation',function(event){doRatio=event.originalEvent.gamma*0.1})}
function snow(){for(i=0;i<flakes.length;i+=1){flakes[i].update()}
snowTimeout=requestAnimationFrame(function(){snow()})}
snow();this.clear=function(){$('.snowfall-canvas').remove();$(element).children('.snowfall-flakes').remove();cancelAnimationFrame(snowTimeout)}};$.fn.snowfall=function(options){if(typeof(options)=="object"||options==undefined){return this.each(function(i){(new $.snowfall(this,options))})}else if(typeof(options)=="string"){return this.each(function(i){var snow=$(this).data('snowfall');if(snow){snow.clear()}})}}})(jQuery)

$("html").snowfall({
    flakeCount : 35,
    flakeColor : '#ffffff',
    flakeIndex: 99999,
    flakePosition: 'absolute',
    minSize : 4,
    maxSize : 8,
    minSpeed : 1,
    maxSpeed : 5,
    round : true,
    shadow : true,
    collection : false,
    image : false,
    collectionHeight : 40
});
"""

def onRevHtml(reviewer, _old):
    res = _old(reviewer)
    return res + "<script>" + js_snow + "</script>"

if not anki21:
    Reviewer._revHtml += "<script>" + js_snow + "</script>"
else:
    Reviewer.revHtml = wrap(Reviewer.revHtml, onRevHtml, pos="around")
