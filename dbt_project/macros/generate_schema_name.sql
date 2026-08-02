{% macro generate_schema_name(custom_schema_name, node) -%}
    {#- Override dbt's default behavior of concatenating <target_schema>_<custom_schema>.
        We want models tagged with +schema: marts to land in exactly `marts`,
        not `staging_marts`. This is a common real-world dbt gotcha worth
        knowing cold if asked "why marts and not staging_marts?" -#}
    {%- if custom_schema_name is not none -%}
        {{ custom_schema_name | trim }}
    {%- else -%}
        {{ target.schema }}
    {%- endif -%}
{%- endmacro %}
