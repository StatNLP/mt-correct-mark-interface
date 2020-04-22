import { h, render, Component } from 'preact';
import PostEdit from './postEdit.js';
import Marking from './marking.js';
import * as sentence from 'sentence';

class UserChoice extends Component {
    constructor() {
        super();
        this.state.selection = null;
        this.postedit_select = this.postedit_select.bind(this);
        this.marking_select = this.marking_select.bind(this);
        this.sentence = sentence;
    }

    postedit_select(e) {
        if (this.state.selection == null) {
            e.preventDefault();
            this.setState({ selection: 'postEdit' });
        }
    }

    marking_select(e) {
        if (this.state.selection == null) {
            e.preventDefault();
            this.setState({ selection: 'marking' });
        }
    }

    render(props, state) {
        var component = null;
        if (state.selection == null) {
            component = <div class="row translation-target"><div id="markingcontainer" class="col text-center">{this.sentence}</div></div>;
        }
        else if (state.selection == 'marking') {
            component = <Marking />;
        }
        else if (state.selection == 'postEdit') {
            component = <PostEdit />;
        }
        return (<div>
            <div class="content-row d-flex justify-content-center">
                <ul class="nav nav-tabs">
                    <li class="nav-item"><a class={'nav-link .bg-info .test-light '.concat((state.selection == 'postEdit') ? 'tab-active' : '')} onClick={this.postedit_select}>Post-Edits</a></li>
                    <li class="nav-item"><a class={'nav-link .bg-info .test-light '.concat((state.selection == 'marking') ? 'tab-active' : '')} onClick={this.marking_select}>Markings</a></li>
                </ul>
            </div>
            {component}
        </div>);
    }
}

export default UserChoice; 
