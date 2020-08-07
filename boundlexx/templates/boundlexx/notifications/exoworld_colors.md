World Colors:
{% for color_group in colors %}
```{% for color in color_group %}
{{ color.item.english|stringformat:"25s" }}: {{ color.color.default_name }} ({{ color.color.game_id }}){% if color.is_new_color %} NEW{% else %}{% if color.exist_via_transform %} TRANSFORM{% endif %}{% if color.days_since_last %} Days: {{ color.days_since_last }}{% endif %}{% endif %}{% endfor %}
```{% if not forloop.last %}%SPLIT_MESSAGE%{% endif %}
{% endfor %}