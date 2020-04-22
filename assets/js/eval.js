import { h, render, Component } from 'preact';  // import { ... } from 'preact';
import * as targets from 'targets';

class Eval extends Component {
    constructor() {
        super();
        this.options = targets;
        this.state.better = null;
        this.state.click_count = 0;
        this.state.time_paused = 0;
        this.state.click_count = 0;
        this.state.paused = false;
        this.state.pause_begin = null;
        this.state.pause_end = null; this.form = document.forms[0];
        this.selection = this.selection.bind(this);
        this.better = document.getElementById('better');
        this.time_started_field = document.getElementById('timestarted');
        this.time_submitted_field = document.getElementById('timesubmitted');
        this.time_paused_field = document.getElementById('timepaused');
        this.click_field = document.getElementById('clicks');
        this.click_counter = this.click_counter.bind(this);
        this.submit = this.submit.bind(this);
        this.pause_resume = this.pause_resume.bind(this);
        this.try_submit = this.try_submit.bind(this);
    }

    componentDidMount() {
        this.time_started_field.value = Date.now().toString();
        document.getElementById('evalParent').focus();
    }

    selection(e) {
        if (this.state.paused == true) {
            return;
        }
        this.setState({ better: e.target.id });
    }

    submit(e) {
        if (this.state.paused) {
            return;
        }
        if (this.state.better == null) {
            return;
        }
        e.preventDefault();
        this.time_submitted_field.value = Date.now().toString();
        this.time_paused_field.value = this.state.time_paused.toString();
        this.click_field.value = this.state.click_count.toString();
        this.better.value = this.state.better.toString();
        this.form.submit();
    }

    click_counter(e) {
        this.setState({ click_count: this.state.click_count + 1 });
    }

    try_submit(e) {
        if (e.keyCode == 13) {
            this.submit(e);
        }
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

    render(props, state) {
        return <div id="evalParent" class="col" tabIndex="0" onKeyDown={this.try_submit} onClick={this.click_counter}>
            <div id="choices" class="row">
                {this.options.map(x =>
                    <div class="evalChoice">
                        <div onClick={this.selection} id={x[0]} class={((state.better == x[0]) ? 'evalSelected' : 'evalLabel')}>{x[1]}</div>
                    </div>)}
            </div>
            <div style="margin-top: 25px;" />
            <div class="row">
                <div class="col">
                    <div class="row d-flex justify-content-center">
                        {(state.paused) ? <button class="btn btn-success" onClick={this.pause_resume}><i class="far fa-play-circle"></i> Continue</button> : <button class="btn btn-danger" onClick={this.pause_resume}><i class="far fa-pause-circle"></i> Pause</button>}
                        <div style="margin-left: 25px; margin-right: 25px;"> </div>
                        <button class="btn btn-primary" onClick={this.submit}>
                            Submit
                        </button>
                    </div>
                </div>
            </div>
        </div>;
    }
}

render(<Eval />, document.getElementById('mountpoint'));