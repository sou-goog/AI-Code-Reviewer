import { Route, Switch } from "wouter";
import Home from "@/pages/Home";
import Stats from "@/pages/Stats";
import History from "@/pages/History";
import Settings from "@/pages/Settings";

function App() {
    return (
        <Switch>
            <Route path="/" component={Home} />
            <Route path="/stats" component={Stats} />
            <Route path="/history" component={History} />
            <Route path="/settings" component={Settings} />
            <Route>404 - Not Found</Route>
        </Switch>
    );
}

export default App;
