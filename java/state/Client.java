package java.state;

import java.util.*;

class Client {
    public static void main(String[] args){
        TrafficLight lightSystem = new TrafficLight();
    }
    
}

/* state */
interface TrafficLightState{
    void changeState(TrafficLight trafficLight);
}

/* concrete State */

class GreenState implements TrafficLightState {
    @Override
    public void changeState(TrafficLight light){
        System.out.println("Green -Go!");
    }
}

class YellowState implements TrafficLightState {
    @Override
    public void changeState(TrafficLight light){
        if (light.getPrevState() instanceof RedState){
            System.out.println("Yellow (from Red to Green) - caution!");
            light.setState(new GreenState());
        }else{
           System.out.println("Yellow (from Green to REd) - caution!");
           light.setState(new RedState());
        }
    }
}

/* concrete state */

class RedState implements TrafficLightState {
    @Override
    public void changeState(TrafficLight light){
        System.out.println("Red - Stop!");
        light.setState(new YellowState());
    }
}

class TrafficLight {
    private TrafficLightState state;
    private TrafficLightState prevState;

    TrafficLight(){
        this.state = new RedState();
        this.prevState = null;
    }

    void setState(TrafficLightState state){
        this.prevState = this.state;
        this.state = state;

    }

    TrafficLightState getPrevState(){
        return this.prevState;
    }

    void change(){
        this.state.changeState(this);
    }

}