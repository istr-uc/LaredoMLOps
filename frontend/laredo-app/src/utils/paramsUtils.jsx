export function validateAndParseParam(parameterName, value, types, enumValues) {
    let isValidParameter = false
    let parsedValue = value

    if (!Array.isArray(types)) {
        types = [types]
    }    

    for (let i = 0; i < types.length; i++) {
        const type = types[i]
        switch(type) {
            case "integer":
                if (Number.isInteger(Number(value))) {
                    parsedValue = parseInt(value, 10)
                    isValidParameter = true
                }
                break
            case "float":
                if (!isNaN(parseFloat(value))) {
                    parsedValue = parseFloat(value)
                    isValidParameter = true
                }
                break
            case "string":
                if (enumValues && Array.isArray(enumValues) && enumValues.length > 0) {
                    if (enumValues.includes(value)) {
                        isValidParameter = true
                    }
                }
                break
            case "boolean":
                if (value === "true" || value === "false" || value === true || value === false) {
                    parsedValue = value === "true" || value === true
                    isValidParameter = true
                }
                break
            case "object":
                if (/^\s*\{.*\}\s*$/.test(value)) {
                    isValidParameter = true
                }
                break
            case "array":
                if (/^\s*\[.*\]\s*$/.test(value)) {
                    isValidParameter = true
                }
                break
            case "null":
                if (value === '' || value === null) {
                    parsedValue = null
                    isValidParameter = true
                }
            default:
                break
        }
        if (isValidParameter === true) {
            break
        }
    }

    return {isValidParameter, parsedValue}
}
