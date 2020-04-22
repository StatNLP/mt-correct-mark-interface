import { h, render, Component } from 'preact';  // import { ... } from 'preact';
import * as sentence from 'sentence';
import ContentEditable from 'react-contenteditable'; 

class PostEdit extends Component {
    constructor() {
        super();
        this.state.original_sentence = sentence;
        this.state.new_sentence = sentence;
        this.state.click_count = 0;
        this.state.keystrokes = 0;
        this.state.paused = false;
        this.state.pause_begin = null;
        this.state.pause_end = null;
        this.state.time_paused = 0;
        this.reset = this.reset.bind(this);
        this.form = document.forms[0];
        this.userchoice_field = document.getElementById('userchoice');
        this.annotation_field = document.getElementById('annotationfield');
        this.time_started_field = document.getElementById('timestarted');
        this.time_submitted_field = document.getElementById('timesubmitted');
        this.time_paused_field = document.getElementById('timepaused');
        this.keystrokes_field = document.getElementById('keystrokes');
        this.click_field = document.getElementById('clicks');
        this.reset = this.reset.bind(this);
        this.handle_update = this.handle_update.bind(this);
        this.click_counter = this.click_counter.bind(this);
        this.submit = this.submit.bind(this);
        this.keystroke_counter = this.keystroke_counter.bind(this);
        this.pause_resume = this.pause_resume.bind(this);
        this.try_submit = this.try_submit.bind(this);
    }

    componentDidMount() {
        this.time_started_field.value = Date.now().toString();
        this.userchoice_field.value = 'postedit';
        this.annotation_field.value = this.state.new_sentence.toString();
    }

    componentDidUpdate() {
        this.annotation_field.value = this.state.new_sentence.toString();
    }

    handle_update(e) {
        if (this.state.paused != true)
        {
            if (e.keyCode == 13) {
                e.preventDefault();
                this.submit(e);
            }
            var newText = e.target.value;
            this.setState({new_sentence: newText});
        }
        else {
            return;
        }
    }

    reset(e) {
        if (this.state.paused != true){
            e.preventDefault();
            this.setState({ new_sentence:       this.state.original_sentence });
        }
        else {
            return;
        }
    }

    submit(e) {
        if (this.state.paused) {
            return;
        }
        e.preventDefault();
        this.time_submitted_field.value = Date.now().toString();
        this.time_paused_field.value = this.state.time_paused.toString();
        this.click_field.value = this.state.click_count.toString();
        this.keystrokes_field.value = this.state.keystrokes.toString();
        this.form.submit();
    }

    click_counter(e) {
        e.preventDefault();
        this.setState({ click_count: this.state.click_count + 1 });
    }

    keystroke_counter(e) {
        this.setState({ keystrokes: this.state.keystrokes + 1 });
    }

    pause_resume(e) {
        if (this.state.paused == false) {
            this.setState({
                paused: true,
                pause_begin: Date.now()
            });
        }
        else {
            var now = Date.now();
            this.setState({
                paused: false,
                pause_end: now,
                time_paused: this.state.time_paused + (now - this.state.pause_begin)
            });
        }
    }

    try_submit(e) {
        if (e.keyCode == 13) {
            this.submit(e);
        }
    }

    render(props, state) {
        return <div class="col align-center" onClick={this.click_counter} onKeyDown={this.keystroke_counter}>
            <ContentEditable html={state.new_sentence} onChange={this.handle_update} disabled={state.paused}className='postedit-area text-center' onKeyDown={this.try_submit}/>
            <div style="margin-top: 25px;"></div>
            <div class="row d-flex justify-content-center">
                {(state.paused) ? <button class="btn btn-success" onClick={this.pause_resume}><i class="far fa-play-circle"></i> Continue</button> : <button class="btn btn-danger" onClick={this.pause_resume}><i class="far fa-pause-circle"></i> Pause</button>}
                <div style="margin-left: 25px; margin-right: 25px;"></div>
                <button class="btn btn-secondary" onClick={this.reset}>Reset</button>
                <div style="margin-left: 25px; margin-right: 25px;"></div>
                <button class="btn btn-primary" onClick={this.submit}>Submit</button>
            </div>
        </div>;
    }
}

export default PostEdit;