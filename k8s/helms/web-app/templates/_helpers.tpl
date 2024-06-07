{{- define "shared.envFrom" }}
{{- range .Values.shared.envFrom }}
  {{- if .configMapRefName }}
  - configMapRef:
      name: {{ .configMapRefName }}
  {{- end }}
  {{- if .secretRefName }}
  - secretRef:
      name: {{ .secretRefName }}
  {{- end }}
{{- end }}
{{- end }}

{{- define "shared.resources" }}
resources:
  limits:
    cpu: {{ .Values.shared.resources.limits.cpu }}
    memory: {{ .Values.shared.resources.limits.memory }}
  requests:
    cpu: {{ .Values.shared.resources.requests.cpu }}
    memory: {{ .Values.shared.resources.requests.memory }}
{{- end }}

{{- define "shared.volumeMounts" }}
volumeMounts:
{{- range .Values.shared.volumeMounts }}
  - name: {{ .name }}
    mountPath: {{ .mountPath }}
{{- end }}
{{- end }}
