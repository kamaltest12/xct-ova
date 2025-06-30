{{/* vim: set filetype=mustache: */}}

{{/*
# Expand the name of the chart.
*/}}
{{- define "test-app.name" -}}
  {{- $var := default .Chart.Name .Values.nameOverride | trunc 63 -}}
  {{- printf "%s" (regexReplaceAllLiteral "[^A-Za-z0-9]*$" $var "") -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "test-app.fullname" -}}
  {{- if .Values.fullnameOverride -}}
    {{- $var := .Values.fullnameOverride | trunc 63 -}}
    {{- printf "%s" (regexReplaceAllLiteral "[^A-Za-z0-9]*$" $var "") -}}
  {{- else -}}
    {{- $name := default .Chart.Name .Values.nameOverride -}}
    {{- if contains $name .Release.Name -}}
      {{- $var := .Release.Name | trunc 63 -}}
      {{- printf "%s" (regexReplaceAllLiteral "[^A-Za-z0-9]*$" $var "") -}}
    {{- else -}}
      {{- $var := printf "%s-%s" .Release.Name $name | trunc 63 -}}
      {{- printf "%s" (regexReplaceAllLiteral "[^A-Za-z0-9]*$" $var "") -}}
    {{- end -}}
  {{- end -}}
{{- end -}}

{{/*
# Create chart name and version as used by the chart label.
*/}}
{{- define "test-app.chart" -}}
  {{- $var := printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 -}}
  {{- printf "%s" (regexReplaceAllLiteral "[^A-Za-z0-9]*$" $var "") -}}
{{- end -}}

# Get rid of scientific notation that could have been introduced by Helm
{{- define "numericSafe" -}}
{{- if . -}}
    {{- if . | toString | contains "e+" -}}
    {{ . | float64 | toString | replace "." "" | regexFind "^\\d+" }}
    {{- else -}}
    {{ . }}
    {{- end -}} 
{{- else -}}
   {{- if eq (toString .) "0" -}}
   {{ "0" }}
   {{- end -}}
{{- end -}}
{{- end -}}


{{- define "booleanSafe" -}}
{{- if . -}}
{{ toString .  }}
{{- else -}}
   {{- if eq (toString .) "false" -}}
   {{ false }}
   {{- end -}}
{{- end -}}
{{- end -}}
