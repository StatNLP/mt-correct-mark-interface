/* eslint-disable no-console */
import { h, render, Component } from 'preact'; // import { ... } from 'preact';
import * as sentence from 'sentence';

class Marking extends Component {
    constructor() {
        super();
        this.state.sentence = sentence;
        this.state.words = sentence.split(' ');
        this.state.selected = this.state.words.map((x) => false);
        this.state.click_count = 0;
        this.state.keystrokes = 0;
        this.state.paused = false;
        this.state.pause_begin = null;
        this.state.pause_end = null;
        this.state.time_paused = 0;
        this.form = document.forms[0];
        this.annotation_field = document.getElementById('annotationfield');
        this.time_started_field = document.getElementById('timestarted');
        this.time_submitted_field = document.getElementById('timesubmitted');
        this.time_paused_field = document.getElementById('timepaused');
        this.click_field = document.getElementById('clicks');
        this.userchoice_field = document.getElementById('userchoice');
        this.keystrokes_field = document.getElementById('keystrokes');
        this.word_click = this.word_click.bind(this);
        this.highlight = this.highlight.bind(this);
        this.click_counter = this.click_counter.bind(this);
        this.keystroke_counter = this.keystroke_counter.bind(this);
        this.submit = this.submit.bind(this);
        this.pause_resume = this.pause_resume.bind(this);
    }

    componentDidMount() {
        this.annotation_field.value = this.state.selected.toString();
        this.time_started_field.value = Date.now().toString();
        this.userchoice_field.value = 'marking';
        document.getElementById('markingParent').focus();
    }

    componentDidUpdate() {
        this.annotation_field.value = this.state.selected.toString();
        console.log(this.state);
    }

    word_click(e) {
        if (this.state.paused) {
            window.getSelection.empty();
            return;
        }
        window.getSelection().empty();
        var selected = this.state.selected;
        selected[parseInt(e.target.id)] = !selected[parseInt(e.target.id)];
        this.setState({ selected: selected });
    }

    highlight(e) {
        if (this.state.paused) {
            window.getSelection.empty();
            return;
        }
        if (e.detail > 1) {
            return;
        }
        var selection = window.getSelection();
        if (selection.isCollapsed) {
            return;
        }
        var beginning = parseInt(selection.anchorNode.parentElement.id);
        var ending = parseInt(selection.focusNode.parentElement.id);
        var selected = this.state.selected;
        var start = beginning;
        var end = ending;
        if (beginning > ending) {
            start = ending;
            end = beginning;
        }
        var setTo = !selected[start];
        var newSelected = selected;
        for (var i = 0; i < newSelected.length; i++) {
            if (i >= start && i <= end) {
                newSelected[i] = setTo;
            }
        }
        selection.empty();
        this.setState({ selected: newSelected });
    }

    submit(e) {
        if (this.state.paused) {
            return;
        }
        e.preventDefault();
        this.time_submitted_field.value = Date.now().toString();
        this.time_paused_field.value = this.state.time_paused.toString();
        this.keystrokes_field.value = this.state.keystrokes.toString();
        this.click_field.value = this.state.click_count.toString();
        this.form.submit();
    }

    click_counter(e) {
        this.setState({ click_count: this.state.click_count + 1 });
    }

    keystroke_counter(e) {
        this.setState({ keystrokes: this.state.keystrokes + 1 });
    }

    try_submit(e) {
        if (e.keyCode == 13) {
            this.submit(e);
        }
    }

    pause_resume(e) {
        if (this.state.paused == false){
            this.setState({
                paused: true,
                pause_begin: Date.now()
            });
            console.log(this.state);
        }
        else {
            var now = Date.now();
            this.setState({
                paused: false,
                pause_end: now,
                time_paused: this.state.time_paused + (now - this.state.pause_begin)
            });
            console.log(this.state);
        }
    }

    render(props, state) {
        return (
            <div id="markingParent" tabIndex="0" onKeyDown={e => { this.keystroke_counter(e); this.try_submit(e); }} onClick={this.click_counter}>
                <div id="markingContainer" class="text-center" onMouseUp={this.highlight}>
                    {state.words.map((word, index) => (
                        <span
                            class={'word'.concat(state.selected[index] ? ' selected' : '')}
                            id={index}
                            onClick={this.word_click}
                        >
                            {word.concat(' ')}
                        </span>
                    ))}
                </div>
                <div style="margin-top: 25px;" />
                <div class="row d-flex justify-content-center">
                    {(state.paused) ? <button class="btn btn-success" onClick={this.pause_resume}><i class="far fa-play-circle"></i> Continue</button> : <button class="btn btn-danger" onClick={this.pause_resume}><i class="far fa-pause-circle"></i> Pause</button>}
                    <div style="margin-left: 25px; margin-right: 25px;"> </div>
                    <button class="btn btn-primary" onClick={this.submit}>
                        Submit
                    </button>
                </div>
            </div>
        );
    }
}

export default Marking;