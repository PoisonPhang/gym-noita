# gym-noita
Repository and pip package for creating an OpenAI environment for training Noita agents.

## Status
Infancy. Nothing is really here yet.  
Documentation for usage will be updated as the project becomes functional.

## Installation
1) Install [OpenAi gym](https://gym.openai.com/docs/)
2) Clone this repository
3) Install package via `pip install -e .`

## Usage
```python
import gym
import gym_noita

env = gym.make('Noita-v0')
```

## Environment

### State update JSON
```json
{ 
  "pos": { 
    "x": 385.95785522461, 
    "y": 301.39401245117 
  }, 
  "hp": 4, 
  "max_hp": 4, 
  "money": 25, 
  "enemies": [  
    { 
      "name": "$animal_blob", 
      "x": 258.60000610352, 
      "y": 511, 
      "has_shot":false 
    }
  ] 
}
```
