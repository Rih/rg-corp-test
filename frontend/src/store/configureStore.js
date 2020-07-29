import { createStore, combineReducers, applyMiddleware } from 'redux'
import { composeWithDevTools } from 'redux-devtools-extension'
import thunk from 'redux-thunk'
import reducers from './reducers'
const rootReducer = combineReducers({
    scraper: reducers
})

const store = createStore(rootReducer, composeWithDevTools(applyMiddleware(thunk)))

export default store
