"""Local console tracing; no collector required."""
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor,ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup(app):
    provider=TracerProvider()
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)
