
# Compara cada prompt con su template

# Usage: ./eval.sh modo
# modo ::= diff o char
# diff: Nos muestra la diferencia de caracteres de cada Prompt con caracteres de su Template
# char: Nos muestra la cantidad total de caracteres de cada Prompt

# De cada prompt existente muestra lo que le pidamos o el nombre del template si no existe
# Los que no existe los muestra por stderr
# Los prompts los saca de reverie/backend_server/logs/prompts

for i in $(ls); do
	ruta_prompt="../../../logs/prompts/$i"
	ruta_template="$i"
	if [ -e "$ruta_prompt" ]; then
		prompt=$(wc -c $ruta_prompt | awk '{print $1}')
		template=$(wc -c $ruta_template | awk '{print $1}')
		diff_a_favor_prompt=$(expr $template - $prompt)
		echo $diff_a_favor_prompt
	else
		echo $ruta_template no ejecutado 1>&2
	fi
done

