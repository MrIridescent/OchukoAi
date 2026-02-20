"""
Phase 4: LLM Function Calling Framework
Structured tool use with schema validation, type checking, and result handling
"""

from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass, asdict
import json
import inspect
from enum import Enum

from logging_system import StructuredLogger

logger = StructuredLogger(__name__)


class ParameterType(Enum):
    """Supported parameter types"""
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"


@dataclass
class Parameter:
    """Function parameter definition"""
    name: str
    type: ParameterType
    description: str
    required: bool = True
    enum_values: Optional[List[str]] = None
    default: Optional[Any] = None
    
    def to_schema(self) -> Dict[str, Any]:
        """Convert to JSON schema"""
        schema = {
            "type": self.type.value,
            "description": self.description,
        }
        if self.enum_values:
            schema["enum"] = self.enum_values
        return schema


@dataclass
class FunctionSpec:
    """LLM-compatible function specification"""
    name: str
    description: str
    parameters: List[Parameter]
    return_type: str = "string"
    
    def to_json_schema(self) -> Dict[str, Any]:
        """Convert to OpenAI function calling schema"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        p.name: p.to_schema()
                        for p in self.parameters
                    },
                    "required": [p.name for p in self.parameters if p.required]
                }
            }
        }


class FunctionRegistry:
    """Registry for callable functions available to LLM"""
    
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        self.specs: Dict[str, FunctionSpec] = {}
    
    def register(self, spec: FunctionSpec, func: Callable):
        """Register function with spec"""
        self.functions[spec.name] = func
        self.specs[spec.name] = spec
        logger.info("Function registered", name=spec.name, parameters=len(spec.parameters))
    
    def get_function(self, name: str) -> Optional[Callable]:
        """Get registered function"""
        return self.functions.get(name)
    
    def get_spec(self, name: str) -> Optional[FunctionSpec]:
        """Get function specification"""
        return self.specs.get(name)
    
    def list_functions(self) -> List[Dict[str, Any]]:
        """Get all functions in JSON schema format"""
        return [self.specs[name].to_json_schema() for name in self.specs]
    
    def get_all_specs(self) -> Dict[str, FunctionSpec]:
        """Get all function specs"""
        return self.specs.copy()


class FunctionCallValidator:
    """Validate function calls against specs"""
    
    @staticmethod
    def validate_call(spec: FunctionSpec, arguments: Dict[str, Any]) -> tuple[bool, Optional[str]]:
        """Validate function call arguments"""
        for param in spec.parameters:
            if param.required and param.name not in arguments:
                return False, f"Missing required parameter: {param.name}"
            
            if param.name in arguments:
                value = arguments[param.name]
                
                if param.type == ParameterType.STRING and not isinstance(value, str):
                    return False, f"Parameter {param.name} must be string"
                
                if param.type == ParameterType.NUMBER and not isinstance(value, (int, float)):
                    return False, f"Parameter {param.name} must be number"
                
                if param.type == ParameterType.INTEGER and not isinstance(value, int):
                    return False, f"Parameter {param.name} must be integer"
                
                if param.type == ParameterType.BOOLEAN and not isinstance(value, bool):
                    return False, f"Parameter {param.name} must be boolean"
                
                if param.enum_values and value not in param.enum_values:
                    return False, f"Parameter {param.name} must be one of {param.enum_values}"
        
        return True, None


class FunctionCallExecutor:
    """Execute function calls with result handling"""
    
    def __init__(self, registry: FunctionRegistry):
        self.registry = registry
        self.validator = FunctionCallValidator()
        self.execution_history: List[Dict[str, Any]] = []
    
    async def execute(
        self,
        function_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute function call and return result"""
        func = self.registry.get_function(function_name)
        spec = self.registry.get_spec(function_name)
        
        if not func:
            return {
                "success": False,
                "error": f"Function not found: {function_name}",
                "function": function_name
            }
        
        valid, error_msg = self.validator.validate_call(spec, arguments)
        if not valid:
            logger.warning("Invalid function call", function=function_name, error=error_msg)
            return {
                "success": False,
                "error": error_msg,
                "function": function_name
            }
        
        try:
            logger.info("Executing function", function=function_name, args_count=len(arguments))
            
            if inspect.iscoroutinefunction(func):
                result = await func(**arguments)
            else:
                result = func(**arguments)
            
            execution_record = {
                "function": function_name,
                "arguments": arguments,
                "result": result,
                "success": True,
                "timestamp": str(__import__('datetime').datetime.utcnow())
            }
            self.execution_history.append(execution_record)
            
            logger.info("Function executed successfully", function=function_name)
            
            return {
                "success": True,
                "function": function_name,
                "result": result
            }
        
        except Exception as e:
            logger.error("Function execution failed", function=function_name, error=str(e))
            return {
                "success": False,
                "error": str(e),
                "function": function_name
            }
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get history of executed functions"""
        return self.execution_history.copy()


class FunctionCallingFramework:
    """Complete framework for LLM function calling"""
    
    def __init__(self):
        self.registry = FunctionRegistry()
        self.executor = FunctionCallExecutor(self.registry)
    
    def register_function(
        self,
        name: str,
        description: str,
        parameters: List[Parameter],
        func: Callable
    ):
        """Register a callable function"""
        spec = FunctionSpec(name, description, parameters)
        self.registry.register(spec, func)
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get tools formatted for LLM function calling"""
        return self.registry.list_functions()
    
    async def call_function(
        self,
        function_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call a registered function"""
        return await self.executor.execute(function_name, arguments)
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get execution history"""
        return self.executor.get_execution_history()


global_function_framework = FunctionCallingFramework()
