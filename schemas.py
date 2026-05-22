from pydantic import BaseModel, ConfigDict, Field

class HabitBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    description: str = Field(min_length=1)
    
class HabitCreate(HabitBase):
    model_config = ConfigDict(from_attributes=True)
    
    frequency_type: str
    goal_value: int

class HabitResponse(HabitBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    created_at: str
    frequency_type: str
    goal_value: int