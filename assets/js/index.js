import { h, render, Component } from 'preact';  // import { ... } from 'preact';
import Marking from './components/marking.js';
import PostEdit from './components/postEdit.js';
import UserChoice from './components/userChoice.js';
import fb_type from 'fb_type';

if (fb_type == 'userchoice') {
    render(<UserChoice />, document.getElementById('mountpoint'));
}
else if (fb_type == 'marking') {
    render(<Marking />, document.getElementById('mountpoint'));
}
else if (fb_type == 'postedit') {
    render(<PostEdit />, document.getElementById('mountpoint'));
}
else {
    render(<div>"System Error, no Feedback Type selected"</div>, document.getElementById('mountpoint'));
}