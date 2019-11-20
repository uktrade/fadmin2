import React from 'react';
import { shallowEqual, useSelector, useDispatch } from 'react-redux';

const Selection = () => {
    const LEFT_TO_RIGHT = 'LEFT_TO_RIGHT';
    const RIGHT_TO_LEFT = 'RIGHT_TO_LEFT';

    const TOP_TO_BOTTOM = 'TOP_TO_BOTTOM';
    const BOTTOM_TO_TOP = 'BOTTOM_TO_TOP';

    const initial = useSelector(state => state.select.initial);
    const last = useSelector(state => state.select.last);
    const useOffset = useSelector(state => state.select.useOffset);

    let horizontalDirection = LEFT_TO_RIGHT;
    let verticalDirection = TOP_TO_BOTTOM;

    let styles = {}

    // Check for select direction
    if (initial.x > last.x) {
        // left to right
        horizontalDirection = RIGHT_TO_LEFT;
    }

    if (initial.y > last.y) {
        // top to bottom
        verticalDirection = BOTTOM_TO_TOP
    }

    let offSetX = 0
    let offSetY = 0

    if (useOffset) {
        offSetX = window.scrollX
        offSetY = window.scrollY
    }

    if (horizontalDirection === LEFT_TO_RIGHT) {
        if (verticalDirection === TOP_TO_BOTTOM) {
            styles = {
                left : initial.x + offSetX,
                top: initial.y + offSetY,
                width: (last.x - initial.x) + initial.width,
                height: (last.y - initial.y) + initial.height
            }
        } else {
            styles = {
                left : initial.x + offSetX,
                top: last.y + offSetY,
                width: (last.x - initial.x) + initial.width,
                height: (initial.y - last.y) + initial.height
            }
        }
    } else { // RIGHT_TO_LEFT
        if (verticalDirection === TOP_TO_BOTTOM) {
            styles = {
                left : last.x + offSetX,
                top: initial.y + offSetY,
                width: (initial.x - last.x) + initial.width,
                height: (last.y - initial.y) + initial.height
            }
        } else {
            styles = {
                left : last.x + offSetX,
                top: last.y + offSetY,
                width: (initial.x - last.x),
                height: (initial.y - last.y)
            }
        }
    }

    return (
        <div style={styles} className="selection"></div>
    )
}

export default Selection;
